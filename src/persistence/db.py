import sqlite3


class BrokingDB:
    def __init__(self):
        self.database_file = f'{__file__}/../../../ebroker.db'

    def get_connection(self):
        """
        Returns connection object
        Returns
        -------
        sqlite3.Connection
        """
        conn = None
        try:
            conn = sqlite3.connect(self.database_file)
        except sqlite3.Error as e:
            print(str(e))
        return conn

    def execute_query(self, query, params=None, is_transactional=False):
        """
        Executes given SQL query and returns the result
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
        conn = self.get_connection()
        if not conn:
            raise Exception('No connection')
        try:
            cur = conn.cursor()
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            if is_transactional:
                conn.commit()
                return []
            else:
                row = cur.fetchall()
                return row
        except Exception as e:
            print(str(e))
            raise Exception('Some error occurred while executing the query')
        finally:
            conn.close()
