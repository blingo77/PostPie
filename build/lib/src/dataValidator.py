# postpie.py
# Copyright (C) 2024 the PostPie developers
# (See DEVELOPERS FILE)

""" 
    Holds all functions used for data validating
"""

allowed_data_types = (
            'VARCHAR', 'INT', 'CHAR', 'TEXT', 'INTEGER', 'BIGINT', 'SMALLINT',
            'NUMERIC', 'DECIMAL', 'UUID', 'TIME', 'INTERVAL', 'TIMESTAMP', 'DATE',
            'REAL', 'BOOLEAN', 'DOUBLE PERCISION'
            )

def check_data_types(kwargs : dict):

    # Checks the values in kwargs for the functions
    # that create tables. Makes sure that their valid
    # data types

    for col, d_type in kwargs.items():
        if d_type.startswith("VARCHAR"):

            try:
                # Grabs the integer value for VARCHAR(###)
                vchar_len = int(d_type[8:-1])

                if vchar_len <= 1 or vchar_len > 255:
                    raise ValueError
                        
            except ValueError:
                raise ValueError(f"ERROR! Invalid VARCHAR length for column name '{col}'")
                    
        elif d_type not in allowed_data_types:
            raise ValueError(f"ERROR! Invalid PostgreSQL datatype for column name '{col}' : {d_type}")

def check_for_string(arg : str):

    # Makes sure if a input for a query is a string
    # Only needed if the specific query requires a string input
    # Psycopg2 will automatically add single quotes around a string
    # during execution of a SQL query.

    # Ex: 'State = NV' --> return True
    #     'State = 1' --> return False

    arg = arg.split()
    arg = "".join(arg)

    for i in range(len(arg)):
        if arg[i] == '=':
            if arg[i + 1].isalpha():
                return True
            else:
                return False
            
def check_for_int(arg : str):

    # Makes sure if a input for a query is a integer
    # Only needed if the specific query requires a integer input

    # Ex: 'id = 1' --> return True
    # Ex: 'id = AZ' --> return False

    arg = arg.split()
    arg = "".join(arg)

    for i in range(len(arg)):
        if arg[i] == '=':
            if arg[i + 1].isdigit():
                return True
            else:
                return False
