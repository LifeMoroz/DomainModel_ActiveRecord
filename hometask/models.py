from hometask.active_record import BaseActiveRecord, Field


class Template(BaseActiveRecord):
    table_name = 'template'
    title = Field()


class Element(BaseActiveRecord):
    table_name = 'element'
    value = Field()


class FieldSubstitution(BaseActiveRecord):
    table_name = 'fieldsubstitution'
    value = Field()


class DE(BaseActiveRecord):
    table_name = 'de'
    document = Field()
    element = Field()
    position = Field()
    _element = Element

    def related_value(self):
        return self._element.find(id=self.element)[0]


class DFS(BaseActiveRecord):
    table_name = 'dfs'
    document = Field()
    fs = Field()
    position = Field()
    _fsub = FieldSubstitution

    def related_value(self):
        return self._fsub.find(id=self.fs)[0]


class Document(BaseActiveRecord):
    table_name = 'document'
    title = Field()
    to_el = DE
    to_fs = DFS

    def clear_template(self):
        conn_elems = self.to_el.find(document=self.id)
        conn_fs = self.to_fs.find(document=self.id)
        for obj in conn_elems + conn_fs:
            obj.delete()

    @property
    def object_list(self):
        conn_elems = self.to_el.find(document=self.id)
        conn_fs = self.to_fs.find(document=self.id)
        items = sorted(conn_elems + conn_fs, key=lambda x: x.position)
        return [it.related_value() for it in items]
