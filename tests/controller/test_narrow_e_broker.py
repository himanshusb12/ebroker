from unittest import TestCase
from unittest.mock import patch
from app import app
from src.service.broking import BrokingService


class EBrokerNarrowIntegrationTest(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_balance_with_missing_params(self):
        response = self.app.get('/broker/api/getBalance?user=1')
        self.assertEqual(response.status_code, 400)
        actual_message = response.get_json()['error']
        self.assertEqual(actual_message, "'userId' not found in request")

    @patch.object(BrokingService, 'get_balance')
    def test_get_balance_with_success(self, mock_get_balance):
        expected_balance = 1234
        mock_get_balance.return_value = expected_balance
        response = self.app.get('/broker/api/getBalance?userId=1')
        self.assertEqual(response.status_code, 200)
        actual_balance = response.get_json()['balance']
        self.assertEqual(actual_balance, expected_balance)

    @patch.object(BrokingService, 'get_balance')
    def test_get_balance_with_unknown_user(self, mock_get_balance):
        error_message = 'No such user exists'
        mock_get_balance.side_effect = [Exception(error_message)]
        response = self.app.get('/broker/api/getBalance?userId=11111')
        self.assertEqual(response.status_code, 500)
        actual_message = response.get_json()['error']
        self.assertEqual(actual_message, error_message)

    def test_add_balance_with_missing_params(self):
        user_id = 1
        amount_to_add = 100
        response = self.app.post('/broker/api/addAmount', json={'userId': user_id, 'Amount': amount_to_add})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], "'amount' not found in request")

    @patch.object(BrokingService, 'add_fund')
    @patch.object(BrokingService, 'get_balance')
    def test_add_balance_with_success(self, mock_get_balance, mock_add_fund):
        mock_get_balance.side_effect = [100, 200]
        mock_add_fund.return_value = 'User balance updated successfully'
        user_id = 1
        amount_to_add = 100
        current_balance = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        response = self.app.post('/broker/api/addAmount', json={'userId': user_id, 'amount': amount_to_add})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'User balance updated successfully')
        new_balance = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        self.assertEqual(new_balance, current_balance + amount_to_add)

    @patch.object(BrokingService, 'add_fund')
    def test_add_balance_with_some_update_error(self, mock_add_fund):
        error_message = 'Some error occurred while updating user balance'
        mock_add_fund.side_effect = [Exception(error_message)]
        user_id = 1
        amount_to_add = 100
        response = self.app.post('/broker/api/addAmount', json={'userId': user_id, 'amount': amount_to_add})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], error_message)

    @patch.object(BrokingService, 'add_fund')
    def test_add_balance_with_negative_amount(self, mock_add_fund):
        error_message = 'Negative amount cannot be added'
        mock_add_fund.side_effect = [Exception(error_message)]
        user_id = 1
        amount_to_add = -100
        response = self.app.post('/broker/api/addAmount', json={'userId': user_id, 'amount': amount_to_add})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], error_message)

    @patch.object(BrokingService, 'add_fund')
    def test_buy_equity_with_negative_shares(self, mock_buy_an_equity):
        error_message = 'Insufficient balance to buy'
        mock_buy_an_equity.side_effect = [Exception(error_message)]
        user_id = 1
        equity_id = 1
        shares_to_buy = 1000000
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], error_message)

    @patch.object(BrokingService, 'buy_an_equity')
    def test_buy_equity_with_insufficient_funds(self, mock_buy_an_equity):
        error_message = 'Insufficient balance to buy'
        mock_buy_an_equity.side_effect = [Exception(error_message)]
        user_id = 1
        equity_id = 1
        shares_to_buy = 1000000
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], error_message)

    @patch.object(BrokingService, 'can_perform_transaction')
    def test_buy_equity_with_not_allowed_date_and_time(self, mock_can_perform_transaction):
        date_error_message = 'You can only buy an equity between Monday and Friday'
        time_error_message = 'You can only buy an equity between 9am and 5pm'
        mock_can_perform_transaction.side_effect = [Exception(date_error_message), Exception(time_error_message)]
        user_id = 1
        equity_id = 1
        shares_to_buy = 1000000
        time_stamp = '12/12/2021 16:00:01'
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], date_error_message)

        time_stamp = '10/12/2021 17:00:01'
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], time_error_message)

    def test_buy_equity_with_missing_params(self):
        user_id = 1
        equity_id = 1
        time_stamp = '12/12/2021 16:00:01'
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], "'numOfShares' not found in request")

    @patch.object(BrokingService, 'buy_an_equity')
    @patch.object(BrokingService, 'get_balance')
    def test_buy_equity_with_success(self, mock_get_balance, mock_buy_an_equity):
        mock_get_balance.side_effect = [200, 150]
        mock_buy_an_equity.return_value = 'Equity bought successfully'
        user_id = 1
        equity_id = 1
        shares_to_buy = 10
        time_stamp = '10/12/2021 16:00:01'
        share_price = 5
        current_balance = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Equity bought successfully')
        new_balance = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        self.assertEqual(new_balance, current_balance - shares_to_buy * share_price)

    def test_sell_equity_with_missing_params(self):
        user_id = 1
        equity_id = 4
        shares_to_buy = 10
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_buy})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], "'timeStamp' not found in request")

    @patch.object(BrokingService, 'sell_an_equity')
    def test_sell_equity_which_user_does_not_hold(self, mocked_sell_an_equity):
        error_message = 'User does not have selected equity'
        mocked_sell_an_equity.side_effect = [Exception(error_message)]
        user_id = 1
        equity_id = 400
        shares_to_buy = 10
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'User does not have selected equity')

    @patch.object(BrokingService, 'sell_an_equity')
    def test_sell_equity_with_insufficient_shares(self, mocked_sell_an_equity):
        error_message = 'Insufficient shares to sell'
        mocked_sell_an_equity.side_effect = [Exception(error_message)]
        user_id = 1
        equity_id = 1
        shares_to_buy = 100000000
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'Insufficient shares to sell')

    @patch.object(BrokingService, 'can_perform_transaction')
    def test_sell_equity_with_not_allowed_date_and_time(self, mocked_can_perform_transaction):
        date_error_message = 'You can only buy an equity between Monday and Friday'
        time_error_message = 'You can only buy an equity between 9am and 5pm'
        mocked_can_perform_transaction.side_effect = [Exception(date_error_message), Exception(time_error_message)]
        user_id = 1
        equity_id = 1
        shares_to_buy = 1000000
        time_stamp = '12/12/2021 16:00:01'
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'You can only buy an equity between Monday and Friday')

        time_stamp = '10/12/2021 17:00:01'
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'You can only buy an equity between 9am and 5pm')

    @patch.object(BrokingService, 'sell_an_equity')
    @patch.object(BrokingService, 'get_balance')
    def test_sell_equity_with_success(self, mocked_get_balance, mocked_sell_an_equity):
        mocked_get_balance.side_effect = [500, 550]
        mocked_sell_an_equity.return_value = 'Equity sold successfully'
        user_id = 1
        equity_id = 1
        shares_to_sell = 10
        time_stamp = '10/12/2021 16:00:01'
        share_price = 5
        current_balance = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_sell, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Equity sold successfully')
        new_balance = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        self.assertEqual(new_balance, current_balance + shares_to_sell * share_price)
