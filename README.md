# ebroker
An eBroker with a single Persona (Trader) with sqlite 2.6.0 database

First steps
-
#### Prerequisite
- Python 3.7.x

- sqlite3 database

#### Installation
1. Create a virtual environment
    ```shell script
    python -m venv venv
    ```

2. Activate the environment
    ```
    venv\Scripts\activate
    ```

3. Install the requirements
    ```
    pip install -r requirements.txt
    ```

4. Set up actual database
    ```
    python setup_db.py
    ```
   This command will create a sqlite database file with name ebroker.db
   
#### Start the API server
Run below command to host the server
    ```
    python app.py
    ```
Server is hosted on http://127.0.0.1:9010

Test and Coverage
-
#### Test cases
1. Run all the tests
    ```
    python -m pytest
    ```
   
2. Run all the tests related to controller layer
    ```
    python -m pytest tests/controller
    ```
   
3. Run all the tests related to service layer
    ```
    python -m pytest tests/service
    ```
   
4. Run all the tests related to persistence layer
    ```
    python -m pytest tests/persistence
    ```

#### Coverage
1. Capture all the coverage
    ```
    coverage run --source=src -m pytest 
    ```
   
2. Get coverage percentage on console
    ```
    coverage report
    ```

3. Generate HTML coverage report
    ```
    coverage html
    ```
    This will create a htmlcov folder in the same directory and coverage report can be accessed by opening htmlcov/index.html file.

API details
-   
1. Get balance
    ##### Request
    ```
   GET      
   http://127.0.0.1:9010/broker/api/getBalance?userId=<user id>
   ```
   ##### Response
   ```json
    {
    "balance": 12000.0,
    "userId": "2"
    }
    ```
   
2. Add amount to user balance
    ##### Request
    ```
   POST      
   http://127.0.0.1:9010/broker/api/addAmount
   
   {
    "userId": 2,
    "amount": 50
    }
   ```
   ##### Response
   ```json
    {
    "message": "User balance updated successfully"
    }
    ```
   
3. Buy an equity
    ##### Request
    ```
   POST      
   http://127.0.0.1:9010/broker/api/buy
   
   {
    "userId": 2,
    "equityId": 1,
    "numOfShares": 10,
    "timeStamp": "10/12/2021 16:00:01"
    }
   ```
   ##### Response
   ```json
    {
    "message": "Equity bought successfully"
    }
    ```
   
4. Sell an equity
    ##### Request
    ```
   POST      
   http://127.0.0.1:9010/broker/api/sell
   
   {
    "userId": 2,
    "equityId": 1,
    "numOfShares": 10,
    "timeStamp": "10/12/2021 16:00:01"
    }
   ```
   ##### Response
   ```json
    {
    "message": "Equity sold successfully"
    }
    ```
