from os import environ
from psycopg2 import connect
import sqlite3
from abc import ABC, abstractmethod


class Database(ABC):
    def __init__(self, host, db_name=None, user=None, psswd=None):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.psswd = psswd

    @property
    @abstractmethod
    def connector(self):
        pass

    @property
    @abstractmethod
    def cursor(self):
        pass


class PostgresDB(Database):
    def __init__(self, host, db_name, user, psswd):
        super().__init__(host, db_name, user, psswd)

    @property
    def connector(self):
        connector = connect(
            host=self.host,
            database=self.db_name,
            user=self.user,
            password=self.psswd,
        )

        connector.autocommit = True
        return connector

    @property
    def cursor(self):
        return self.connector.cursor()


class SQLiteDB(Database):
    def __init__(self, host):
        super().__init__(host)

    @property
    def connector(self):
        return sqlite3.connect(self.host)

    @property
    def cursor(self):
        return self.connector.cursor()
