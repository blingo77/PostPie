# postpie.py
# Copyright (C) 2024 the PostPie developers
# (See DEVELOPERS FILE)

import psycopg2
from psycopg2 import pool



def connect(config):

    global DB_CONFIG

    DB_CONFIG.update(config)


DB_CONFIG = {
    'database' : '',
    'user' : '',
    'password' : '',
    'host' : '',
    'port' : ''
}

pool = pool.SimpleConnectionPool(minconn=1, maxconn=10, **DB_CONFIG)

def get_data_from_database():
    with pool.getconn() as conn:  # Get a connection from the pool
        with conn.cursor() as cur:  # Create a cursor object
            cur.execute("SELECT * FROM customer")
            return cur.fetchall()
        
data = get_data_from_database()

print(data)