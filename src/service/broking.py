import datetime
from src.persistence.user import UserRepository
from src.persistence.equity import EquityRepository
from src.persistence.user_equity_map import UserEquityMapRepository


class BrokingService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.equity_repository = EquityRepository()
        self.map_repository = UserEquityMapRepository()

    @staticmethod
    def can_perform_transaction(time_stamp):
        """
        Checks whether an equity can be bought or sold from 9 to 5 and Monday to Friday
        Parameters
        ----------
        time_stamp: str
            request timestamp

        Returns
        -------
        bool
        """
        date_time = datetime.datetime.strptime(time_stamp, '%d/%m/%Y %H:%M:%S')
        # Between 9 am and 5 pm
        if date_time.time() < datetime.time(9, 0, 0) or date_time.time() > datetime.time(17, 0, 0):
            raise Exception('You can only buy an equity between 9am and 5pm')
        # Monday is 0 and Sunday is 6
        if date_time.weekday() > 4:
            raise Exception('You can only buy an equity between Monday and Friday')
        return True

    def buy_an_equity(self, user_id, equity_id, num_of_shares, time_stamp):
        """
        Buys given num of shares of an equity for a given user
        Parameters
        ----------
        user_id: int
            id of the user who is buying the shares
        equity_id: int
            id of the equity user is buying
        num_of_shares: int
            num of shares to buy
        time_stamp: str
            date and time at which this transaction is happening

        Returns
        -------
        str
        """
        if num_of_shares < 0:
            raise Exception('Provide non negative number of shares to buy')
        if num_of_shares == 0:
            raise Exception('Provide minimum one share to buy')
        self.can_perform_transaction(time_stamp)
        user_info = self.user_repository.get_user(user_id)
        current_balance = user_info[2]
        equity_info = self.equity_repository.get_equity(equity_id)
        equity_price = equity_info[2]
        total_amount_to_deduct = equity_price * num_of_shares
        if current_balance < total_amount_to_deduct:
            raise Exception('Insufficient balance to buy')
        user_equity_map_id = self.map_repository.get_user_equity_mapping_id(user_id, equity_id)
        if user_equity_map_id is not None:
            user_equity_info = self.map_repository.get_user_equity(user_equity_map_id)
            total_shares = num_of_shares + user_equity_info[3]
            updated_user_equity = {
                'id': user_equity_map_id,
                'user_id': user_id,
                'equity_id': equity_id,
                'total_shares': total_shares
            }
            self.map_repository.update_equity(updated_user_equity)
        else:
            total_shares = num_of_shares
            updated_user_equity = {
                'user_id': user_id,
                'equity_id': equity_id,
                'total_shares': total_shares
            }
            self.map_repository.add_user_equity(updated_user_equity)
        updated_user = {
            'id': user_id,
            'name': user_info[1],
            'balance': current_balance - total_amount_to_deduct
        }
        self.user_repository.update_user(updated_user)
        return 'Equity bought successfully'

    def sell_an_equity(self, user_id, equity_id, num_of_shares, time_stamp):
        """
        Sells given num of shares of an equity for a given user
        Parameters
        ----------
        user_id: int
            id of the user who is selling the shares
        equity_id: int
            id of the equity user is selling
        num_of_shares: int
            num of shares to sell
        time_stamp: str
            date and time at which this transaction is happening

        Returns
        -------
        str
        """
        if num_of_shares < 0:
            raise Exception('Provide non negative number of shares to sell')
        if num_of_shares == 0:
            raise Exception('Provide minimum one share to sell')
        self.can_perform_transaction(time_stamp)
        user_equity_map_id = self.map_repository.get_user_equity_mapping_id(user_id, equity_id)
        if not user_equity_map_id:
            raise Exception('User does not have selected equity')
        else:
            user_equity_info = self.map_repository.get_user_equity(user_equity_map_id)
            total_shares = user_equity_info[3]
            if total_shares < num_of_shares:
                raise Exception('Insufficient shares to sell')
            equity_info = self.equity_repository.get_equity(equity_id)
            equity_price = equity_info[2]
            total_amount_to_add = equity_price * num_of_shares
            user_info = self.user_repository.get_user(user_id)
            current_balance = user_info[2]
            if total_shares == num_of_shares:
                self.map_repository.delete_user_equity_map(user_equity_map_id)
            else:
                updated_user_equity = {
                    'id': user_equity_map_id,
                    'user_id': user_id,
                    'equity_id': equity_id,
                    'total_shares': total_shares - num_of_shares
                }
                self.map_repository.update_equity(updated_user_equity)
            updated_user = {
                'id': user_id,
                'name': user_info[1],
                'balance': current_balance + total_amount_to_add
            }
            self.user_repository.update_user(updated_user)
            return 'Equity sold successfully'

    def add_fund(self, user_id, amount):
        """
        Add given amount to user balance
        Parameters
        ----------
        user_id: int
            id of the user
        amount: float
            amount to add

        Returns
        -------
        str
        """
        if amount < 0:
            raise Exception('Negative amount cannot be added')
        user_result = self.user_repository.get_user(user_id)
        if user_result is None:
            raise Exception('No such user exists')
        user = {
            'id': user_id,
            'name': user_result[1],
            'balance': user_result[2] + amount
        }
        if not self.user_repository.update_user(user):
            raise Exception('Some error occurred while updating user balance')
        return 'User balance updated successfully'

    def get_balance(self, user_id):
        """
        Returns current balance of a user
        Parameters
        ----------
        user_id: int
            id of the user

        Returns
        -------
        float
        """
        user = self.user_repository.get_user(user_id)
        if user is None:
            raise Exception('No such user exists')
        current_balance = user[2]
        return current_balance
