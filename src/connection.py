# postpie.py
# Copyright (C) 2024 the PostPie developers
# (See DEVELOPERS FILE)

import psycopg2
from psycopg2 import pool

class Connect:
    pool = None

    @classmethod
    def init(cls, data_base, db_user, db_password, db_host, db_port : int, minconn=1, maxconn=10):
        DB_CONFIG = {
            'database' : f'{data_base}',
            'user' : f'{db_user}',
            'password' : f'{db_password}',
            'host' : f'{db_host}',
            'port' : db_port
        }
        cls.pool = pool.SimpleConnectionPool(minconn, maxconn, **DB_CONFIG)
