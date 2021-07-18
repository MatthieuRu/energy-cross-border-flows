import pandas as pd
import sqlalchemy
from database import DataBase
from sqlalchemy.sql import text
from typing_extensions import Literal


class Server:
    """A Server database.
    """

    def __init__(self, ip, user, passwd, database) -> None:
        """
        Args:
            name (string): name of the table
            db (DataBase): parent database
        Attrs:
            name (string): name of the table
            db (DataBase): parent database
            server (Server): parent server
        """
        self.ip = ip
        self.database = database
        self.user = user
        self.passwd = passwd
        self.connection = self._get_connection()
        self.db = self._get_databases()

    def _get_databases(self):
        """ Get all the database which can be used by the user,
            from the server.
        """
        return {
            x: DataBase(x, self)
            for x in self._show_databases()["schema_name"]
            if x
            not in ["information_schema", "pg_catalog", "pg_toast", "piblic"]
        }

    def _get_connection(self):
        """ Connect to the server and database
        """
        conn_str = f"postgres+psycopg2://{self.user}:{self.passwd}@{self.ip}:5432/{self.database}"
        engine = sqlalchemy.create_engine(conn_str)
        return engine.connect()

    def _execute_extract(self, action):
        """ Execute an extract query (response from server)
        """
        return pd.read_sql(action, self.connection)

    def _execute_action(self, action):
        """ Execute an action query (no response from server)
        """
        self.connection.execute(action)
        return 1

    def _show_databases(self):
        """ Excute the query to get all the database from a
            specicifics server
        """
        return self._execute_extract(
            "select schema_name from information_schema.schemata;"
        )

    def _create_schema(self, filename: str) -> Literal[1]:
        """ Generate the a .sql file from a file
        """
        file = open(filename)
        query = text(file.read())
        self._execute_action(query)
        self.db = self._get_databases()
        return 1

    def _delete_schema(self) -> Literal[1]:
        """ Delete the dexter schema if needed
        """
        query = """drop schema dexter cascade;"""
        self._execute_action(query)
        self.db = self._get_databases()
        return 1
