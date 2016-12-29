from hometask.active_record import BaseActiveRecord, Field


class Element(BaseActiveRecord):
    """
    Класс элемента, наследуется от класса BaseActiveRecord
    """
    table_name = 'element'  # имя таблицы
    value = Field()  # в базе будет поле value  # в базе будет поле value


class FieldSubstitution(BaseActiveRecord):
    """
    Класс подставновки, наследуется от класса BaseActiveRecord
    """
    table_name = 'fieldsubstitution'  # имя таблицы
    value = Field()  # в базе будет поле value 


class DE(BaseActiveRecord):
    """
    Класс для разрешения связи между Document и Element
    """
    table_name = 'de'  # имя таблицы
    document = Field()  # в базе будет поле document
    element = Field()  # в базе будет поле element
    position = Field()  # в базе будет поле position
    _element = Element  # класс с которым образуется связь

    def related_value(self):  # Получаем значение связанного элемента
        return self._element.find(id=self.element)[0]


class DFS(BaseActiveRecord):
    """
    Класс для разрешения связи между Document и FieldSubstitution
    """
    table_name = 'dfs'  # имя таблицы
    document = Field()  # в базе будет поле document
    fs = Field()  # в базе будет поле fs
    position = Field()  # в базе будет поле position
    _fsub = FieldSubstitution  # класс с которым образуется связь

    def related_value(self):  # Получаем значение связанной подстановки
        return self._fsub.find(id=self.fs)[0]


TEMPLATE_CHOICES = ['doc', 'html', 'txt']  # Список возможных форматов шаблона


class Document(BaseActiveRecord):
    table_name = 'document'  # имя таблицы
    title = Field()  # в базе будет поле title
    template = Field()  # в базе будет поле template
    to_el = DE  # класс-связь с элементами
    to_fs = DFS  # класс-связь с подстановками

    def clear_template(self):  # Очищаем связи шаблона
        conn_elems = self.to_el.find(document=self.id)  # Связанные элементы
        conn_fs = self.to_fs.find(document=self.id)  # Связанные подстановки
        for obj in conn_elems + conn_fs:  # для всех связей
            obj.delete()  # удаляем

    @property
    def object_list(self):  # Получить список всех элементов и подстановок, отсортированных по их позиции
        conn_elems = self.to_el.find(document=self.id)  # связанные элементы
        conn_fs = self.to_fs.find(document=self.id)  # связанные подстановки
        items = sorted(conn_elems + conn_fs, key=lambda x: x.position)  # сортируем по позиции
        return [it.related_value() for it in items]  # Возвращаем список элементов и подстановок

    def save(self):  # Перегрузка метода save super-класса
        if self.template not in TEMPLATE_CHOICES:  # Проверяем, что такой формат существует и входит в список допустимых
            raise ValueError('Нет такого формата')  # Показываем ошибку
        return super().save()  # Вызываем метод super-класса
