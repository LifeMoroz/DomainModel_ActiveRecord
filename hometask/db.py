import sqlite3
from django.conf import settings


class Database:
    db = None

    def __init__(self):
        self._conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
        self._cursor = self._conn.cursor()

    @staticmethod
    def get_database():
        return Database()

    @staticmethod
    def execute(sql, params=None, unescape=None):
        self = Database.get_database()
        sql = sql.format(unescape) if unescape else sql
        try:
            if params:
                return self._cursor.execute(sql, params)
            else:
                return self._cursor.execute(sql)
        finally:
            self._conn.commit()

