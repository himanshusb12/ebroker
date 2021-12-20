import os
import sqlite3
from sqlite3 import Error


def create_connection(database_file):
    """
    Creates a database connection to a SQLite database
    """
    conn = None
    try:
        conn = sqlite3.connect(database_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_tables(conn):
    """
    Creates required tables for ebroker
    """
    query = """CREATE TABLE IF NOT EXISTS users 
                (
                    id integer PRIMARY KEY,
                    name text NOT NULL,
                    balance real NOT NULL,
                    last_modified_on text NOT NULL
                );"""
    cur = conn.cursor()
    cur.execute(query)

    query = """CREATE TABLE IF NOT EXISTS equities 
                    (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        price real NOT NULL,
                        last_modified_on text NOT NULL
                    );"""
    cur = conn.cursor()
    cur.execute(query)

    query = """CREATE TABLE IF NOT EXISTS user_equity_map 
                        (
                            id integer PRIMARY KEY,
                            user_id integer,
                            equity_id integer,
                            total_shares integer NOT NULL,
                            last_modified_on text NOT NULL,
                            FOREIGN KEY(user_id) REFERENCES users(id),
                            FOREIGN KEY(equity_id) REFERENCES equities(id)
                        );"""
    cur = conn.cursor()
    cur.execute(query)


def fill_testing_data(conn):
    """
    Inserts data in newly created tables
    """
    query = """INSERT INTO users (name, balance, last_modified_on) VALUES (?, ?, datetime('now'))"""
    data = [('Dummy', 10000), ('Himanshu', 12000)]
    cur = conn.cursor()
    for d_row in data:
        cur.execute(query, d_row)
    conn.commit()

    query = """INSERT INTO equities (name, price, last_modified_on) VALUES (?, ?, datetime('now'))"""
    data = [('ITC', 5), ('TCS', 10), ('SBIN', 12), ('INFY', 15), ('AXISBANK', 20)]
    cur = conn.cursor()
    for d_row in data:
        cur.execute(query, d_row)
    conn.commit()

    query = """INSERT INTO user_equity_map (user_id, equity_id, total_shares, last_modified_on) 
                VALUES (?, ?, ?, datetime('now'))"""
    data = [(1, 1, 10), (1, 2, 10), (1, 3, 10), (1, 4, 10), (1, 5, 10), (2, 1, 10), (2, 2, 10), (2, 3, 10)]
    cur = conn.cursor()
    for d_row in data:
        cur.execute(query, d_row)
    conn.commit()


if __name__ == '__main__':
    database_file = r'ebroker.db'
    if os.path.exists(database_file):
        delete = input('A database file already exists. '
                       'Do you want me to delete the existing one and create a new one? (y/n):\t')
        if delete.lower() in ('y', 'yes'):
            os.remove(database_file)
        else:
            print('Skipping the set up as database already exists. If you still want to set up a fresh database then'
                  ' delete the existing database - ebroker.db')
            exit()
    conn = create_connection(database_file)
    if conn:
        create_tables(conn)
        fill_testing_data(conn)
        conn.close()
        print('Database setup done')