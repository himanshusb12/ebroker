from .db import BrokingDB


class EquityRepository:
    def __init__(self):
        """
        Class to perform CRUD operation on equity table
        """
        self.db = BrokingDB()

    def get_equity(self, equity_id):
        query = 'SELECT id, name, price FROM equities WHERE id = ?'
        result_set = self.db.execute_query(query, (equity_id,))
        if len(result_set):
            return result_set[0]
        else:
            return None

    def get_all_equities(self):
        query = 'SELECT id, name, price FROM equities'
        result_set = self.db.execute_query(query)
        return result_set

    def add_equity(self, equity):
        name = equity['name']
        price = equity['price']
        query = "INSERT INTO equities (name, price, last_modified_on) VALUES (?, ?, datetime('now'))"
        self.db.execute_query(query, (name, price), is_transactional=True)
        return True

    def delete_equity(self, equity_id):
        query = 'DELETE FROM equities WHERE id = ?'
        self.db.execute_query(query, (equity_id, ), is_transactional=True)
        return True

    def update_equity(self, equity):
        equity_id = equity['id']
        equity_name = equity['name']
        equity_price = equity['price']
        query = "UPDATE equities SET name=?, price = ?, last_modified_on = datetime('now') where id = ?"
        self.db.execute_query(query, (equity_name, equity_price, equity_id), is_transactional=True)
        return True
