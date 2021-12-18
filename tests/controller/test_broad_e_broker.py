from unittest import TestCase
from app import app


class EBrokerBroadIntegrationTest(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_add_balance_with_unknown_user(self):
        user_id = 1111111
        amount_to_add = 100
        response = self.app.post('/broker/api/addAmount', json={'userId': user_id, 'amount': amount_to_add})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'No such user exists')

    def test_buy_equity_with_zero_and_negative_shares_to_buy(self):
        user_id = 1
        equity_id = 1
        shares_to_buy = -10
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'Provide non negative number of shares to buy')

        shares_to_buy = 0
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'Provide minimum one share to buy')

    def test_buy_equity_with_insufficient_funds(self):
        user_id = 1
        equity_id = 1
        shares_to_buy = 10000000
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'Insufficient balance to buy')

    def test_buy_equity_with_not_allowed_date_and_time(self):
        user_id = 1
        equity_id = 1
        shares_to_buy = 1000000
        time_stamp = '12/12/2021 16:00:01'
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'You can only buy an equity between Monday and Friday')

        time_stamp = '10/12/2021 17:00:01'
        response = self.app.post('/broker/api/buy', json={'userId': user_id, 'equityId': equity_id,
                                                          'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'You can only buy an equity between 9am and 5pm')

    def test_sell_equity_with_zero_and_negative_shares_to_sell(self):
        user_id = 1
        equity_id = 1
        shares_to_buy = -10
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'Provide non negative number of shares to sell')

        shares_to_buy = 0
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'Provide minimum one share to sell')

    def test_sell_equity_which_user_does_not_hold(self):
        user_id = 1
        equity_id = 1001
        shares_to_buy = 10
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'User does not have selected equity')

    def test_sell_equity_with_insufficient_shares(self):
        user_id = 1
        equity_id = 1
        shares_to_buy = 1000000
        time_stamp = '10/12/2021 16:00:01'
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_buy, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'Insufficient shares to sell')

    def test_sell_equity_with_not_allowed_date_and_time(self):
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

    def test_add_buy_and_sell(self):
        user_id = 1
        equity_id = 1
        amount_to_add = 50
        current_balance = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        response = self.app.post('/broker/api/addAmount', json={'userId': user_id, 'amount': amount_to_add})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'User balance updated successfully')
        balance_after_adding_the_amount = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        self.assertEqual(balance_after_adding_the_amount, current_balance + amount_to_add)

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

        shares_to_sell = 10
        current_balance = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        response = self.app.post('/broker/api/sell', json={'userId': user_id, 'equityId': equity_id,
                                                           'numOfShares': shares_to_sell, 'timeStamp': time_stamp})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'Equity sold successfully')
        new_balance = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        self.assertEqual(new_balance, current_balance + shares_to_sell * share_price)

        latest_balance = self.app.get(f'/broker/api/getBalance?userId={user_id}').get_json()['balance']
        self.assertEqual(latest_balance, balance_after_adding_the_amount)

