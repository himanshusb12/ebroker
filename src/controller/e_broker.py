from flask import request, jsonify
from flask.blueprints import Blueprint
from src.service.broking import BrokingService

broker_api = Blueprint('broker', __name__)


@broker_api.route('/buy', methods=['POST'])
def buy():
    try:
        request_body = request.json
        user_id = request_body['userId']
        equity_id = request_body['equityId']
        num_of_shares = request_body['numOfShares']
        time_stamp = request_body['timeStamp']
        service = BrokingService()
        return jsonify({'message': service.buy_an_equity(user_id, equity_id, num_of_shares, time_stamp)}), 200
    except KeyError as e:
        return jsonify({'error': f'{str(e)} not found in request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@broker_api.route('/sell', methods=['POST'])
def sell():
    try:
        request_body = request.json
        user_id = request_body['userId']
        equity_id = request_body['equityId']
        num_of_shares = request_body['numOfShares']
        time_stamp = request_body['timeStamp']
        service = BrokingService()
        return jsonify({'message': service.sell_an_equity(user_id, equity_id, num_of_shares, time_stamp)}), 200
    except KeyError as e:
        return jsonify({'error': f'{str(e)} not found in request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@broker_api.route('/addAmount', methods=['POST'])
def add():
    try:
        request_body = request.json
        user_id = request_body['userId']
        amount = request_body['amount']
        service = BrokingService()
        return jsonify({'message': service.add_fund(user_id, amount)}), 200
    except KeyError as e:
        return jsonify({'error': f'{str(e)} not found in request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@broker_api.route('/getBalance', methods=['GET'])
def balance():
    try:
        user_id = request.args['userId']
        service = BrokingService()
        user_balance = service.get_balance(int(user_id))
        return jsonify({'userId': user_id, 'balance': user_balance}), 200
    except KeyError:
        return jsonify({'error': f"'userId' not found in request"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
