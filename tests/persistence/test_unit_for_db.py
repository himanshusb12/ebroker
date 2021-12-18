import sqlite3
from unittest import TestCase
from unittest.mock import MagicMock, patch
from src.persistence.db import BrokingDB


class TestDB(TestCase):
    def setUp(self):
        self.db = BrokingDB()

    @patch.object(sqlite3, 'connect')
    def test_error_while_connecting(self, mocked_connect):
        error_message = 'No proper DB file found'
        mocked_connect.side_effect = Exception(error_message)
        with self.assertRaisesRegex(Exception, error_message):
            conn = self.db.get_connection()
            self.assertIsNone(conn)

    def test_proper_connection(self):
        self.assertIsNotNone(self.db.get_connection())

    @patch.object(BrokingDB, 'get_connection')
    def test_execute_query_with_no_connection(self, mocked_connect):
        mocked_connect.return_value = None
        query = 'SELECT id FROM users'
        with self.assertRaisesRegex(Exception, 'No connection'):
            self.db.execute_query(query)

    @patch.object(BrokingDB, 'get_connection')
    def test_execute_query_for_select_statement(self, mocked_connect):
        expected_result = [(1,)]
        mocked_cursor = MagicMock()
        mocked_cursor.fetchall.return_value = expected_result
        conn = MagicMock()
        conn.cursor.return_value = mocked_cursor
        mocked_connect.return_value = conn
        query = 'SELECT id FROM users'
        actual_result = self.db.execute_query(query)
        self.assertEqual(expected_result, actual_result)

    @patch.object(BrokingDB, 'get_connection')
    def test_execute_query_for_select_statement_with_where_clause(self, mocked_connect):
        expected_result = [(10,)]
        mocked_cursor = MagicMock()
        mocked_cursor.fetchall.return_value = expected_result
        conn = MagicMock()
        conn.cursor.return_value = mocked_cursor
        mocked_connect.return_value = conn
        query = 'SELECT id FROM users WHERE id = ?'
        actual_result = self.db.execute_query(query, params=(10, ))
        self.assertEqual(expected_result, actual_result)

    @patch.object(BrokingDB, 'get_connection')
    def test_execute_query_for_update_statement(self, mocked_connect):
        expected_result = []
        mocked_cursor = MagicMock()
        mocked_cursor.fetchall.return_value = expected_result
        conn = MagicMock()
        conn.cursor.return_value = mocked_cursor
        mocked_connect.return_value = conn
        query = 'UPDATE users SET balance = ? WHERE id = ?'
        actual_result = self.db.execute_query(query, params=(100, 1), is_transactional=True)
        self.assertEqual(expected_result, actual_result)

    @patch.object(BrokingDB, 'get_connection')
    def test_execute_query_for_error_while_executing_update_statement(self, mocked_connect):
        expected_message = 'Some error occurred while executing the query'
        conn = MagicMock()
        conn.cursor.side_effect = [Exception()]
        mocked_connect.return_value = conn
        query = 'UPDATE users SET balance = ? WHERE id = ?'
        with self.assertRaisesRegex(Exception, expected_message):
            self.db.execute_query(query, params=(100, 1), is_transactional=True)
