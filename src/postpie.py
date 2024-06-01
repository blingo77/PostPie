# postpie.py
# Copyright (C) 2024 the PostPie developers
# (See DEVELOPERS FILE)
 
import psycopg2

def hello():
    print('hello')

class PostPie:

    """ 
    The PostPie object is powered by the psycopg2 driver library to connect and
    execute PostgreSQL code. All main functions can be found under the PostPie object.

    Users must connect to their PostgreSQL database in the following way:

    Ex: py = PostPie(host_name='', db_name='', db_user='', db_password='', db_port='')

    Replace '' with the according database credentials.

    Any function that has **kwargs, the KEY should be the column name and
    the VALUE should be the datatype for the column or the value according
    to the function that is being used.

    Ex: name='VARCHAR(255)' OR name='John Doe'
    """

    # User must Connect to their PostgreSQL server with these credentials
    def __init__(self, host_name, db_name, db_user, db_password, db_port):
        self.connection = psycopg2.connect(host=host_name, dbname=db_name, user=db_user, password=db_password, port=db_port)
        self.allowed_data_types = (
            'VARCHAR', 'INT', 'CHAR', 'TEXT', 'INTEGER', 'BIGINT', 'SMALLINT',
            'NUMERIC', 'DECIMAL', 'UUID', 'TIME', 'INTERVAL', 'TIMESTAMP', 'DATE',
            'REAL', 'BOOLEAN', 'DOUBLE PERCISION'
            )

    def create_table(self, tableName: str, **kwargs):
        
        # CREATES A TABLE IF IT DOSENT EXIST ALREADY 
        # A id will be automatically made into the primary key for the table

        with self.connection.cursor() as cursor:

            # column_names will hold both: names of the column and datatype
            # ex. name DATATYPE(), name DATATYPE, name DATATYPE
            coulmn_names = ", ".join([f"{cols} {kwargs[cols]}" for cols in kwargs])

            # Checks if the inputed data type is a valid PostgreSQL data type
            # allowed data types are stored in the allowed_data_types set()
            for col, d_type in kwargs.items():
                if d_type.startswith("VARCHAR"):

                    try:
                        # Grabs the integer value for VARCHAR(###)
                        vchar_len = int(d_type[8:-1])

                        if vchar_len <= 1 or vchar_len > 255:
                            raise ValueError
                        
                    except ValueError:
                        raise ValueError(f"ERROR! Invalid VARCHAR length for column name '{col}'")
                    
                elif d_type not in self.allowed_data_types:
                    raise ValueError(f"ERROR! Invalid PostgreSQL datatype for column name '{col}' : {d_type}")

            try:
                cursor.execute(f""" CREATE TABLE IF NOT EXISTS {tableName} ( id SERIAL PRIMARY KEY, {coulmn_names}) """, list(kwargs.values()))
            
            except SyntaxError:
                raise SyntaxError("ERROR! SQL Query could not execute due to a SYNTAX ERROR")
            
            print("Table successfully created!")
            self.connection.commit() 

    def show_table(self, tableName : str):

        # show_table will only print the table to the terminal
        # this function will not return anything, see/use show_custom_table_info 
        # to have a table or row returned

        with self.connection.cursor() as cursor:

            cursor.execute(f""" SELECT * FROM {tableName} ;""")

            rows = cursor.fetchall()
            for i in rows:
                print(i)

    def show_custom_table_info(self, tableName : str, *args, where=None) -> tuple:

        # SHOWS TABLE INFORMATION BASED ON *args 
        # show_custom_table_info also returns the data in the row as a tuple

        with self.connection.cursor() as cursor:

            # Joins the columns that are inputed through *args
            # If there is no arguments passed, '*' will be the column
            columns = ", ".join(args) if args else "*"
            where_str = "" if where is None else f" WHERE {where}"

            try:
                cursor.execute(f""" SELECT {columns} FROM {tableName} {where_str}""")

            # No table found or exists error
            except psycopg2.errors.UndefinedTable:
                pass
            
            rows = cursor.fetchall()

            for row in rows:
                print(row)

            return rows

    def insert(self, tableName : str, **kwargs):

        # Inserts a new row into a table

        with self.connection.cursor() as cursor:

            # The column values will look like '%s, %s, %,s' when passed into the string
            values = ", ".join([f"%s" for i in kwargs])
            columns = ", ".join(kwargs.keys())

            # list(kwargs.values()) will be placed into the %s placeholders on execution
            cursor.execute(f""" INSERT INTO {tableName} ({columns}) VALUES ({values}); """, list(kwargs.values()))

            print('New row inserted successfully!')
            self.connection.commit()

    def delete_row_by_id(self, tableName : str, id : int):

        # Deletes a row by row ID

        with self.connection.cursor() as cursor:

            # %s is the place holder for ID, [id] will be passed into %s
            cursor.execute(f""" DELETE FROM {tableName} WHERE id = %s """, [id])

            print(f'Row {id} deleted successfully!')
            self.connection.commit()


    def drop_table(self, tableName : str):

        # Deletes all data and the table itself off the planet
        # Confirms that the user actually wants to drop the table from the planet
        while True:
            confirm = input(f"Are you sure you would like to drop table: {tableName}, (Y - Yes / N - No): ").capitalize()

            if confirm == 'Y': break
            else: return

        with self.connection.cursor() as cursor:
            cursor.execute(f""" DROP TABLE {tableName} """)

            print(f'Table {tableName} was dropped successfully')
            self.connection.commit()
        
    
    def get_by_id(self, tableName : str, id : int, column : str):

        # RETURNS A SINGLE VALUE BASED ON ID AND column
        # ID needs to be a primary key ID

        with self.connection.cursor() as cursor:

            try:

                cursor.execute(f""" SELECT  {column} FROM {tableName} WHERE id = %s; """, [id])
                row = cursor.fetchone()
                return row[0]
            
            except TypeError:
                raise TypeError('ERROR! ID or COLUMN can not be found')

    
    def get_row_by_id(self, tableName : str, id : int,  *args) -> tuple:

        with self.connection.cursor() as cursor:

            columns = " , ".join(args) if args else '*'
            cursor.execute(f""" SELECT {columns} FROM {tableName} WHERE id = %s; """, [id])

            return cursor.fetchone()

    def update_by_id(self, tableName: str, ID : int, **kwargs):

        # Updates a row by ID
        #If needing to update an ID, pass the ID by lowercase ID (id)

        with self.connection.cursor() as cursor:

            # %s is a placeholer for the column values it will be placed in the string
            # when the SQL command is executed
            columns_values = ", ".join([f"{col} = %s" for col in kwargs])

            # list(kwargs.values()) holds the dictionary values that will be placed in 
            # the place holders %s where column_values are, the [id] will placed into id = %s
            cursor.execute( f"UPDATE {tableName} SET {columns_values} WHERE id = %s;", list(kwargs.values()) + [ID])
            self.connection.commit()

    def add_column(self, tableName: str, **kwargs):

        # Adds a colum to an existing table

        with self.connection.cursor() as cursor:

            # colum will look hold the column name then colum data type
            # Ex. kwargs = name='VARCHAR(255)' -> 'name VARCHAR(255)'
            column = ", ".join([f"{col} {kwargs[col]}" for col in kwargs])

            try:

                cursor.execute(f""" ALTER TABLE {tableName} ADD COLUMN {column} """)

            except SyntaxError:
                raise SyntaxError('ERROR! Syntax Error')

            print(f'Column added successfully!')
            self.connection.commit()
    
    def drop_column(self, tableName : str, columnName : str):
        
        # Drops a column from the table
        with self.connection.cursor() as cursor:

            try:
                cursor.execute(f""" ALTER TABLE {tableName} DROP COLUMN {columnName} """)

            except psycopg2.errors.UndefinedColumn:
                raise psycopg2.errors.UndefinedColumn

            print(f'Column {columnName} dropped successfully!')
            self.connection.commit()

    def create_foreign_key_table(self, tableName, fk_name=None, **kwargs):

        # The Foriegn Key must be an ID which is a primary key
        
        # The Foriegn Key must be formatted as follows: 
        # Contains the tables name followed by _id
        # Ex: user_id

        if fk_name == None:
            raise TypeError("ERROR! No foreign key was provided")

        with self.connection.cursor() as cursor:

            columns = ", ".join([f'{col} {kwargs[col]} ' for col in kwargs])
            fk_alterName = ''

            # Grabs the name of the foriegn key without the _id part
            for i in fk_name:
                if i == '_':
                    break
                fk_alterName += i

            for col, d_type in kwargs.items():
                if d_type.startswith("VARCHAR"):

                    try:
                        # Grabs the integer value for VARCHAR(###)
                        vchar_len = int(d_type[8:-1])

                        if vchar_len <= 1 or vchar_len > 255:
                            raise ValueError
                        
                    except ValueError:
                        raise ValueError(f"ERROR! Invalid VARCHAR length for column name '{col}'")
                    
                elif d_type not in self.allowed_data_types:
                    raise ValueError(f"ERROR! Invalid PostgreSQL datatype for column name '{col}' : {d_type}")

            try:
                cursor.execute(f""" CREATE TABLE {tableName} ( id SERIAL PRIMARY KEY, {columns}, 
                            {fk_name} INT, CONSTRAINT fk_{fk_alterName} FOREIGN KEY({fk_name}) REFERENCES {fk_alterName}(id)); """)
            except:
                print()
            
            print(f'Table with foreign key successfully created!')
            self.connection.commit()
    
    def add_foreign_key(self, tableName, fk_name=None):
        
        with self.connection.cursor() as cursor:

            fk_alterName = ''

            # Grabs the name of the foriegn key without the _id part
            for i in fk_name:
                if i == '_':
                    break
                fk_alterName += i

            cursor.execute(f""" ALTER TABLE {tableName} ADD CONSTRAINT fk_{fk_alterName} FOREIGN KEY({fk_name}) REFERENCES {fk_alterName}(id)""")

            self.connection.commit()

py = PostPie(host_name='localhost', db_name='postgres', db_user='postgres', db_password='MasterGaming1',db_port=5432)
py.show_table('customer')
