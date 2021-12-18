from .db import BrokingDB


class UserEquityMapRepository:
    def __init__(self):
        """
        Class to perform CRUD operation on user_equity_map table
        """
        self.db = BrokingDB()

    def get_user_equity(self, user_equity_id):
        query = 'SELECT id, user_id, equity_id, total_shares FROM user_equity_map WHERE id = ?'
        result_set = self.db.execute_query(query, (user_equity_id,))
        if len(result_set):
            return result_set[0]
        else:
            return None

    def get_user_equity_mapping_id(self, user_id, equity_id):
        query = 'SELECT id FROM user_equity_map WHERE user_id = ? AND equity_id = ?'
        result_set = self.db.execute_query(query, (user_id, equity_id))
        if len(result_set):
            return result_set[0][0]
        else:
            return None

    def add_user_equity(self, user_equity):
        user_id = user_equity['user_id']
        equity_id = user_equity['equity_id']
        total_shares = user_equity['total_shares']
        query = "INSERT INTO user_equity_map (user_id, equity_id, total_shares, last_modified_on)" \
                " VALUES (?, ?, ?, datetime('now'))"
        self.db.execute_query(query, (user_id, equity_id, total_shares), is_transactional=True)
        return True

    def delete_user_equity_map(self, user_equity_map_id):
        query = "DELETE FROM user_equity_map WHERE id = ?"
        self.db.execute_query(query, (user_equity_map_id,), is_transactional=True)
        return True

    def update_equity(self, user_equity):
        user_equity_map_id = user_equity['id']
        user_id = user_equity['user_id']
        equity_id = user_equity['equity_id']
        total_shares = user_equity['total_shares']
        query = "UPDATE user_equity_map SET user_id = ?, equity_id = ?, total_shares = ?, " \
                "last_modified_on = datetime('now') where id = ?"
        self.db.execute_query(query, (user_id, equity_id, total_shares, user_equity_map_id), is_transactional=True)
        return True
