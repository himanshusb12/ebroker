from flask import Flask
from src.controller.e_broker import broker_api

app = Flask(__name__)

app.register_blueprint(broker_api, url_prefix='/broker/api')

if __name__ == '__main__':
    app.run(port=9010)