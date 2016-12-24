from hometask.db import Database


class Field:
    pass


class BaseActiveRecord:
    table_name = None
    id = Field()  # PK by default

    def __init__(self, *args, **kwargs):
        # Умная сборка объекта. Все что передано проставляем в объект.
        # Наследники будут определять что должно быть.
        if args:
            for i, key in enumerate(self.fields()):
                setattr(self, key, args[i])

        elif kwargs:
            for key in self.__dir__():
                if isinstance(getattr(self, key), Field):
                    setattr(self, key, kwargs.get(key))
        else:
            raise Exception

    @classmethod
    def fields(cls):
        fields = []
        for key in dir(cls):
            if isinstance(getattr(cls, key), Field):
                fields.append(key)
        return fields

    @classmethod
    def find(cls, **kwargs):
        """

        :param kwargs:
        :return: list(gateway)
        """
        where = ''
        data = []
        for key, value in kwargs.items():
            if where:
                where += ' and '
            else:
                where = 'WHERE '
            if isinstance(value, list):
                where += '{} IN ({})'.format(key, ', '.join([str(x) for x in value]))
            else:
                where += '{}=?'.format(key)
                data.append(value)
        sql = "SELECT {fields} FROM {table_name} {where}".format(fields=', '.join(cls.fields()), table_name=cls.table_name, where=where)
        result = []
        for row in Database.get_database().execute(sql, data).fetchall():
            result.append(cls(*row))
        return result

    def save(self):
        to_save = {}
        for key in self.fields():
            to_save[key] = getattr(self, key)
            if key == 'id' and to_save[key] is None:  # Получаем новый id
                to_save['id'] = max([x.id for x in self.find()] or [0]) + 1
        fields = ', '.join(to_save.keys())
        values = ':' + ', :'.join(to_save.keys())
        sql = "REPLACE INTO {table_name} ({fields}) VALUES ({values})"
        sql = sql.format(table_name=self.table_name, fields=fields, values=values)
        Database.get_database().execute(sql, to_save)

    def delete(self):
        sql = "DELETE FROM {table_name} WHERE id={id}".format(table_name=self.table_name, id=self.id)
        Database.get_database().execute(sql)
