from pandas import DataFrame


class Table:
    """A Postgres table.
    """

    def __init__(self, name: str, db) -> None:
        """
        Args:
            name (str): name of the table
            db (DataBase): parent database
        Attrs:
            name (string): name of the table
            db (DataBase): parent database
            server (Server): parent server
        """
        self.name = name
        self.db = db
        self.server = db.server

    def append_dataframe(self, df: DataFrame) -> int:
        """[summary]

        Args:
            df (DataFrame): [description]

        Returns:
            bool: 0 if it didn't work / 1 if it works
        """
        self.db.start_engine()
        try:
            df.to_sql(
                self.name,
                self.db.engine,
                schema=self.db.name,
                if_exists="append",
                index=False,
                method="multi",
            )
        except Exception as e:
            print(e.args[0])
            raise ValueError("I have raised an Exception")
        self.db.stop_engine()
        return 1

