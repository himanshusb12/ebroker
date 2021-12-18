from .db import BrokingDB


class UserRepository:
    def __init__(self):
        """
        Class to perform CRUD operation on user table
        """
        self.db = BrokingDB()

    def get_user(self, user_id):
        query = 'SELECT id, name, balance FROM users WHERE id = ?'
        result_set = self.db.execute_query(query, (user_id,))
        if len(result_set):
            return result_set[0]
        else:
            return None

    def get_all_users(self):
        query = 'SELECT id, name, balance FROM users'
        result_set = self.db.execute_query(query)
        return result_set

    def add_user(self, user):
        name = user['name']
        balance = user['balance']
        query = "INSERT INTO users (name, balance, last_modified_on) VALUES (?, ?, datetime('now'))"
        self.db.execute_query(query, (name, balance), is_transactional=True)
        return True

    def delete_user(self, user_id):
        query = 'DELETE FROM users WHERE id = ?'
        self.db.execute_query(query, (user_id, ), is_transactional=True)
        return True

    def update_user(self, user):
        user_id = user['id']
        user_name = user['name']
        amount = user['balance']
        query = "UPDATE users SET name=?, balance = ?, last_modified_on = datetime('now') where id = ?"
        self.db.execute_query(query, (user_name, amount, user_id), is_transactional=True)
        return True
