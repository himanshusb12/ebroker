from src.persistence.db import BrokingDB


IN_MEMORY_DB = ':memory:'


class InMemoryDB(BrokingDB):
    def __init__(self):
        """
        Class to perform db operation on an in-memory database
        """
        super().__init__()
        self.database_file = IN_MEMORY_DB
        self.conn = self.get_connection()

    def create_tables(self):
        """
        Creates required tables for in-memory database
        """
        query = """CREATE TABLE IF NOT EXISTS users 
                    (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        balance real NOT NULL,
                        last_modified_on text NOT NULL
                    );"""
        cur = self.conn.cursor()
        cur.execute(query)

        query = """CREATE TABLE IF NOT EXISTS equities 
                        (
                            id integer PRIMARY KEY,
                            name text NOT NULL,
                            price real NOT NULL,
                            last_modified_on text NOT NULL
                        );"""
        cur = self.conn.cursor()
        cur.execute(query)

        query = """CREATE TABLE IF NOT EXISTS user_equity_map 
                            (
                                id integer PRIMARY KEY,
                                user_id integer,
                                equity_id integer,
                                total_shares integer NOT NULL,
                                last_modified_on text NOT NULL,
                                FOREIGN KEY(user_id) REFERENCES users(id),
                                FOREIGN KEY(equity_id) REFERENCES equities(id)
                            );"""
        cur = self.conn.cursor()
        cur.execute(query)

    def execute_query(self, query, params=None, is_transactional=False):
        """
        Executes given SQL query and returns the result. An in-memory db exists till the connection is available. With
        each new connection a new in-memory db is created.
        Parameters
        ----------
        query: str
            SQL query
        params: tuple
            values to be passed in SQL query at run time
        is_transactional: bool
            whether the given query performs some data manipulation like insert, delete, update

        Returns
        -------
        list of tuple
        """
        if not self.conn:
            raise Exception('No connection')
        try:
            cur = self.conn.cursor()
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            if is_transactional:
                self.conn.commit()
                return []
            else:
                row = cur.fetchall()
                return row
        except Exception as e:
            print(str(e))
            raise Exception('Some error occurred while executing the query')
