from sqlalchemy import create_engine
from table import Table
import pandas as pd
from typing import List


class DataBase:
    """A Postgres database.
    """

    def __init__(self, name: str, server) -> None:
        """
        Args:
            name (str): name of the database
            server (Server): parent server
        Attrs:
            name (str): name of the database
            server(Server): parent server
            tb (dict): dict of the tables on the database 
                {name (str) : table (Table)}
        """
        self.name = name
        self.server = server
        self.tb = {x: Table(x, self) for x in self._get_tables()["tablename"]}

    def _get_tables(self) -> pd.DataFrame:
        """ Get the tables from this database
        """
        return self.server._execute_extract(
            "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = '{}'".format(
                self.name
            )
        )

    def show_tables(self) -> List[str]:
        """ Get the name of all tables from this database.
        """
        return list(self.tb.keys())

    def start_engine(self) -> None:
        """ Start the connection between user and the database.
        """
        cmd = f"postgres+psycopg2://{self.server.user}:{self.server.passwd}@{self.server.ip}:5432/{self.server.database}"
        self.engine = create_engine(cmd)
        self.engine_state = "started"

    def stop_engine(self) -> None:
        """ Stope the connection between user and the database.
        """
        self.engine.dispose()
        self.engine_state = "stopped"
