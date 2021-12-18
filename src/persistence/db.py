import sqlite3


class BrokingDB:
    def __init__(self):
        self.database_file = f'{__file__}/../../../ebroker.db'

    def get_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database_file)
        except sqlite3.Error as e:
            print(str(e))
        return conn

    def execute_query(self, query, params=None, is_transactional=False):
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
