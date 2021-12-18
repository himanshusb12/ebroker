from unittest import TestCase
from src.persistence.user import UserRepository
from src.persistence.equity import EquityRepository
from src.persistence.user_equity_map import UserEquityMapRepository


class TestBroadIntegrationForUser(TestCase):
    def setUp(self):
        self.user_repository = UserRepository()

    def test_proper_connection(self):
        self.assertIsNotNone(self.user_repository.db.get_connection())

    def test_get_and_update_user_details(self):
        user_info = self.user_repository.get_user(user_id=1)
        expected_name = 'Dummy'
        self.assertEqual(expected_name, user_info[1])
        new_balance = 99999
        user = dict(zip(['id', 'name', 'balance'], user_info))
        user['balance'] = new_balance
        self.assertTrue(self.user_repository.update_user(user))
        updated_user_info = self.user_repository.get_user(user_id=1)
        self.assertEqual(expected_name, updated_user_info[1])
        self.assertEqual(new_balance, updated_user_info[2])
        user['balance'] = user_info[2]
        self.assertTrue(self.user_repository.update_user(user))

    def test_no_user_found(self):
        user_info = self.user_repository.get_user(user_id=9999999999999999)
        self.assertIsNone(user_info)


class TestBroadIntegrationForEquity(TestCase):
    def setUp(self):
        self.equity_repository = EquityRepository()

    def test_proper_connection(self):
        self.assertIsNotNone(self.equity_repository.db.get_connection())

    def test_get_and_update_equity_details(self):
        equity_info = self.equity_repository.get_equity(equity_id=1)
        expected_name = 'ITC'
        expected_price = 5
        self.assertEqual(expected_name, equity_info[1])
        self.assertEqual(expected_price, equity_info[2])
        new_price = 100
        equity = dict(zip(['id', 'name', 'price'], equity_info))
        equity['price'] = new_price
        self.assertTrue(self.equity_repository.update_equity(equity))
        updated_equity_info = self.equity_repository.get_equity(equity_id=1)
        self.assertEqual(expected_name, updated_equity_info[1])
        self.assertEqual(new_price, updated_equity_info[2])
        equity['price'] = equity_info[2]
        self.assertTrue(self.equity_repository.update_equity(equity))

    def test_no_equity_found(self):
        user_info = self.equity_repository.get_equity(equity_id=9999999999999999)
        self.assertIsNone(user_info)


class TestBroadIntegrationForUserEquityMap(TestCase):
    def setUp(self):
        self.map_repository = UserEquityMapRepository()

    def test_proper_connection(self):
        self.assertIsNotNone(self.map_repository.db.get_connection())

    def test_get_and_update_user_equity_mapping(self):
        user_equity_map_id = self.map_repository.get_user_equity_mapping_id(user_id=1, equity_id=1)
        self.assertIsNotNone(user_equity_map_id)
        user_equity_info = self.map_repository.get_user_equity(user_equity_map_id)
        expected_shares = 10
        self.assertEqual(expected_shares, user_equity_info[3])
        new_map = dict(zip(['id', 'user_id', 'equity_id', 'total_shates'], user_equity_info))
        new_shares = 100
        new_map['total_shares'] = new_shares
        self.assertTrue(self.map_repository.update_equity(new_map))
        updated_user_equity_info = self.map_repository.get_user_equity(user_equity_map_id)
        self.assertEqual(new_shares, updated_user_equity_info[3])
        new_map['total_shares'] = user_equity_info[3]
        self.assertTrue(self.map_repository.update_equity(new_map))

    def test_no_equity_found_for_user(self):
        user_info = self.map_repository.get_user_equity_mapping_id(user_id=9999999999999999, equity_id=9999999999999999)
        self.assertIsNone(user_info)

    def test_no_user_equity_for_given_id(self):
        user_equity_info = self.map_repository.get_user_equity(user_equity_id=9999999999999999)
        self.assertIsNone(user_equity_info)