# postpie.py
# Copyright (C) 2024 the PostPie developers
# (See DEVELOPERS FILE)

import psycopg2
from postpie import PostPie

class Joins(PostPie):
    def __init__(self, host_name, db_name, db_user, db_password, db_port):
        super().__init__(host_name=host_name, db_name=db_name, db_user=db_user, db_password=db_password, db_port=db_port)




