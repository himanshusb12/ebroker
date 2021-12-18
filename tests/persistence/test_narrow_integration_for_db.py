from unittest import TestCase
from src.persistence.in_memory import InMemoryDB
from src.persistence.user import UserRepository
from src.persistence.equity import EquityRepository
from src.persistence.user_equity_map import UserEquityMapRepository


# IN_MEMORY_DB = ':memory:'


class TestNarrowIntegrationForUser(TestCase):
    def setUp(self):
        in_memory_db = InMemoryDB()
        in_memory_db.create_tables()
        self.user_repository = UserRepository()
        self.user_repository.db = in_memory_db
        self.equity_repository = EquityRepository()
        self.equity_repository.db = in_memory_db
        self.map_repository = UserEquityMapRepository()
        self.map_repository.db = in_memory_db

    def test_proper_connection(self):
        self.assertIsNotNone(self.user_repository.db.conn)

    def test_create_get_update_and_delete_user(self):
        # create a user
        user = {
            'name': 'tester',
            'balance': 1234
        }
        self.assertTrue(self.user_repository.add_user(user))
        all_users = self.user_repository.get_all_users()
        self.assertEqual(len(all_users), 1)
        new_user_id = list(filter(lambda u: u[1] == 'tester', all_users))[0][0]
        # get user info
        new_user_info = self.user_repository.get_user(new_user_id)
        self.assertEqual(new_user_info[0], new_user_id)
        self.assertEqual(new_user_info[1], 'tester')
        self.assertEqual(new_user_info[2], 1234)
        # update user info
        new_user = dict(zip(['id', 'name', 'balance'], new_user_info))
        new_user['balance'] = 9876
        self.assertTrue(self.user_repository.update_user(new_user))
        updated_user_info = self.user_repository.get_user(new_user_id)
        self.assertEqual(updated_user_info[2], 9876)
        # delete user
        self.assertTrue(self.user_repository.delete_user(new_user_id))
        all_users = self.user_repository.get_all_users()
        self.assertEqual(len(all_users), 0)

    def test_create_get_update_and_delete_equity(self):
        # create an equity
        equity = {
            'name': 'myEquity',
            'price': 100
        }
        self.assertTrue(self.equity_repository.add_equity(equity))
        all_equities = self.equity_repository.get_all_equities()
        self.assertEqual(len(all_equities), 1)
        new_equity_id = list(filter(lambda e: e[1] == 'myEquity', all_equities))[0][0]
        # get equity info
        new_equity_info = self.equity_repository.get_equity(new_equity_id)
        self.assertEqual(new_equity_info[0], new_equity_id)
        self.assertEqual(new_equity_info[1], 'myEquity')
        self.assertEqual(new_equity_info[2], 100)
        # update equity info
        new_equity = dict(zip(['id', 'name', 'price'], new_equity_info))
        new_equity['price'] = 250
        self.assertTrue(self.equity_repository.update_equity(new_equity))
        updated_user_info = self.equity_repository.get_equity(new_equity_id)
        self.assertEqual(updated_user_info[2], 250)
        # delete equity
        self.assertTrue(self.equity_repository.delete_equity(new_equity_id))
        all_users = self.equity_repository.get_all_equities()
        self.assertEqual(len(all_users), 0)

    def test_create_get_update_and_delete_equity_for_a_user(self):
        # create a user and an equity
        user = {
            'name': 'tester',
            'balance': 1234
        }
        self.user_repository.add_user(user)
        equity = {
            'name': 'myEquity',
            'price': 100
        }
        self.equity_repository.add_equity(equity)
        all_users = self.user_repository.get_all_users()
        user_id = list(filter(lambda u: u[1] == 'tester', all_users))[0][0]
        all_equities = self.equity_repository.get_all_equities()
        equity_id = list(filter(lambda e: e[1] == 'myEquity', all_equities))[0][0]
        total_shares = 15
        user_equity_map = {
            'user_id': user_id,
            'equity_id': equity_id,
            'total_shares': total_shares
        }
        self.map_repository.add_user_equity(user_equity_map)
        user_equity_id = self.map_repository.get_user_equity_mapping_id(user_id, equity_id)
        self.assertIsNotNone(user_equity_id)
        # get map info
        user_equity_info = self.map_repository.get_user_equity(user_equity_id)
        user_equity_info = dict(zip(['id', 'user_id', 'equity_id', 'total_shares'], user_equity_info))
        self.assertEqual(user_equity_info['user_id'], user_id)
        self.assertEqual(user_equity_info['equity_id'], equity_id)
        self.assertEqual(user_equity_info['total_shares'], total_shares)
        # update map info
        new_shares = 20
        user_equity_info['total_shares'] = new_shares
        self.assertTrue(self.map_repository.update_equity(user_equity_info))
        updated_user_equity_info = self.map_repository.get_user_equity(user_equity_id)
        self.assertEqual(updated_user_equity_info[3], new_shares)
        # delete map info
        self.assertTrue(self.map_repository.delete_user_equity_map(user_equity_id))
        user_equity_id = self.map_repository.get_user_equity_mapping_id(user_id, equity_id)
        self.assertIsNone(user_equity_id)
