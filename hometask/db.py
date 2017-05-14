import sqlite3
from django.conf import settings


class Database:
    """
    Класс обертка над базой, изолирует инициализацию БД и курсора
    """
    db = None

    def __init__(self, path):
        self._conn = sqlite3.connect(path)
        self._cursor = self._conn.cursor()

    @classmethod
    def get_database(cls, path):  # Несовместимые с клиентами интерфейс
        return ProjectDatabase(path)

    @classmethod
    def execute(cls, sql, params=None, unescape=None):
        self = ProjectDatabase.get_database()
        sql = sql.format(unescape) if unescape else sql
        try:
            if params:
                return self._cursor.execute(sql, params)
            else:
                return self._cursor.execute(sql)
        finally:
            self._conn.commit()


class ProjectDatabase(Database):
    @classmethod
    def get_database(cls):  # Приводим к совместимому
        return ProjectDatabase(settings.DATABASES['default']['NAME'])
