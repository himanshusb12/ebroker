from builtins import map
from unittest import TestCase
from unittest.mock import MagicMock

from src.service.broking import BrokingService


class TestBrokingService(TestCase):
    def setUp(self):
        self.service = BrokingService()
        self.service.user_repository = MagicMock()
        self.service.equity_repository = MagicMock()
        self.service.map_repository = MagicMock()
        self.user_id = 1

    def test_can_perform_transaction_before_9am(self):
        current_time_stamp = '11/12/2021 08:16:24'
        expected_message = 'You can only buy an equity between 9am and 5pm'
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.can_perform_transaction(current_time_stamp)

    def test_can_perform_transaction_after_5pm(self):
        current_time_stamp = '11/12/2021 17:00:01'
        expected_message = 'You can only buy an equity between 9am and 5pm'
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.can_perform_transaction(current_time_stamp)

    def test_can_perform_transaction_on_saturday(self):
        current_time_stamp = '11/12/2021 16:00:01'
        expected_message = 'You can only buy an equity between Monday and Friday'
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.can_perform_transaction(current_time_stamp)

    def test_can_perform_transaction_on_sunday(self):
        current_time_stamp = '12/12/2021 16:00:01'
        expected_message = 'You can only buy an equity between Monday and Friday'
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.can_perform_transaction(current_time_stamp)

    def test_can_perform_transaction_on_monday_between_9_and_5(self):
        current_time_stamp = '10/12/2021 16:00:01'
        self.assertTrue(self.service.can_perform_transaction(current_time_stamp))

    def test_buy_an_equity_with_negative_shares_to_buy(self):
        expected_message = 'Provide non negative number of shares to buy'
        current_time_stamp = '10/12/2021 16:00:01'
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.buy_an_equity(user_id=1, equity_id=1, num_of_shares=-100,
                                       time_stamp=current_time_stamp)

    def test_buy_an_equity_with_zero_shares_to_buy(self):
        expected_message = 'Provide minimum one share to buy'
        current_time_stamp = '10/12/2021 16:00:01'
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.buy_an_equity(user_id=1, equity_id=1, num_of_shares=0,
                                       time_stamp=current_time_stamp)

    def test_buy_an_equity_with_insufficient_funds(self):
        expected_message = 'Insufficient balance to buy'
        current_time_stamp = '10/12/2021 16:00:01'
        self.service.user_repository.get_user.return_value = (1, 'mocked', 900)
        self.service.equity_repository.get_equity.return_value = (1, 'mocked', 10)
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.buy_an_equity(user_id=1, equity_id=1, num_of_shares=100,
                                       time_stamp=current_time_stamp)

    def test_buy_more_existing_equity_with_sufficient_funds(self):
        expected_message = 'Equity bought successfully'
        current_time_stamp = '10/12/2021 16:00:01'
        self.service.user_repository.get_user.return_value = (1, 'mocked', 1100)
        self.service.equity_repository.get_equity.return_value = (1, 'mocked', 10)
        self.service.map_repository.get_user_equity_mapping_id.return_value = 1
        actual_message = self.service.buy_an_equity(user_id=1, equity_id=1, num_of_shares=100,
                                                    time_stamp=current_time_stamp)
        self.assertEqual(actual_message, expected_message)

    def test_buy_an_equity_for_the_first_time_with_sufficient_funds(self):
        expected_message = 'Equity bought successfully'
        current_time_stamp = '10/12/2021 16:00:01'
        self.service.user_repository.get_user.return_value = (1, 'mocked', 1100)
        self.service.equity_repository.get_equity.return_value = (1, 'mocked', 10)
        self.service.map_repository.get_user_equity_mapping_id.return_value = None
        actual_message = self.service.buy_an_equity(user_id=1, equity_id=1, num_of_shares=100,
                                                    time_stamp=current_time_stamp)
        self.assertEqual(actual_message, expected_message)

    def test_sell_an_equity_with_negative_shares_to_sell(self):
        expected_message = 'Provide non negative number of shares to sell'
        current_time_stamp = '10/12/2021 16:00:01'
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.sell_an_equity(user_id=1, equity_id=1, num_of_shares=-100,
                                        time_stamp=current_time_stamp)

    def test_sell_an_equity_with_zero_shares_to_sell(self):
        expected_message = 'Provide minimum one share to sell'
        current_time_stamp = '10/12/2021 16:00:01'
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.sell_an_equity(user_id=1, equity_id=1, num_of_shares=0,
                                        time_stamp=current_time_stamp)

    def test_sell_non_holding_equity(self):
        expected_message = 'User does not have selected equity'
        current_time_stamp = '10/12/2021 16:00:01'
        self.service.map_repository.get_user_equity_mapping_id.return_value = None
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.sell_an_equity(user_id=1, equity_id=1, num_of_shares=100,
                                        time_stamp=current_time_stamp)

    def test_sell_an_equity_with_insufficient_shares(self):
        expected_message = 'Insufficient shares to sell'
        current_time_stamp = '10/12/2021 16:00:01'
        self.service.map_repository.get_user_equity_mapping_id.return_value = 1
        self.service.map_repository.get_user_equity.return_value = (1, 1, 1, 99)
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.sell_an_equity(user_id=1, equity_id=1, num_of_shares=100,
                                        time_stamp=current_time_stamp)

    def test_sell_an_equity_with_sufficient_shares(self):
        expected_message = 'Equity sold successfully'
        current_time_stamp = '10/12/2021 16:00:01'
        self.service.map_repository.get_user_equity_mapping_id.return_value = 1
        self.service.map_repository.get_user_equity.return_value = (1, 1, 1, 199)
        actual_message = self.service.sell_an_equity(user_id=1, equity_id=1, num_of_shares=100,
                                                     time_stamp=current_time_stamp)
        self.assertEqual(actual_message, expected_message)

    def test_sell_all_the_shares_of_an_equity(self):
        expected_message = 'Equity sold successfully'
        current_time_stamp = '10/12/2021 16:00:01'
        self.service.map_repository.get_user_equity_mapping_id.return_value = 1
        self.service.map_repository.get_user_equity.return_value = (1, 1, 1, 100)
        actual_message = self.service.sell_an_equity(user_id=1, equity_id=1, num_of_shares=100,
                                                     time_stamp=current_time_stamp)
        self.assertEqual(actual_message, expected_message)

    def test_add_funds(self):
        expected_message = 'User balance updated successfully'
        self.service.user_repository.get_user.return_value = (1, 'mocked', 1000)
        actual_message = self.service.add_fund(user_id=1, amount=1000)
        self.assertEqual(actual_message, expected_message)

    def test_add_funds_with_negative_amount(self):
        expected_message = 'Negative amount cannot be added'
        self.service.user_repository.update_user.return_value = False
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.add_fund(user_id=1, amount=-1000)

    def test_add_funds_with_some_error(self):
        expected_message = 'Some error occurred while updating user balance'
        self.service.user_repository.update_user.return_value = False
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.add_fund(user_id=1, amount=1000)

    def test_get_balance_for_unknown_user(self):
        expected_message = 'No such user exists'
        self.service.user_repository.get_user.return_value = None
        with self.assertRaisesRegex(Exception, expected_message):
            self.service.get_balance(user_id=99999)

    def test_get_balance(self):
        expected_amount = 1000
        self.service.user_repository.get_user.return_value = (1, 'mocked', expected_amount)
        actual_amount = self.service.get_balance(user_id=99999)
        self.assertEqual(expected_amount, actual_amount)
