# %s is used as place holders for column values 
import psycopg2

class PostPie:

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

        with self.connection.cursor() as cursor:

            values = ", ".join([f"%s" for i in kwargs])
            columns = ", ".join(kwargs.keys())

            cursor.execute(f""" INSERT INTO {tableName} ({columns}) VALUES ({values}); """, list(kwargs.values()))

            self.connection.commit()

    def delete_row_by_id(self, tableName : str, id : int):
        cursor = self.connection.cursor()

        cursor.execute(f""" DELETE FROM {tableName} WHERE id = {id}; """)

        self.connection.commit()

        self.connection.close()
        cursor.close()


    def drop_table(self, tableName : str):
        cursor = self.connection.cursor()

        cursor.execute(f""" DROP TABLE {tableName}; """)

        self.connection.commit()

        self.connection.close()
        cursor.close()
    
    def get_by_id(self, tableName : str, id : int, column : str):

        """ RETURNS A SINGLE VALUE BASED ON ID AND column"""

        cursor = self.connection.cursor()

        cursor.execute(f""" SELECT  {column} FROM {tableName} WHERE id = {id}; """)

        row = cursor.fetchone()

        cursor.close()
        self.connection.close()

        return row[0]
    
    def get_row_by_id(self, tableName : str, id : int,  *args) -> tuple:

        with self.connection.cursor() as cursor:

            columns = " , ".join(args) if args else '*'
            cursor.execute(f""" SELECT {columns} FROM {tableName} WHERE id = %s; """, [id])

            return cursor.fetchone()

    def update_by_id(self, tableName: str, id : int, **kwargs):

        with self.connection.cursor() as cursor:

            # %s is a placeholer for the column values it will be placed in the string
            # when the SQL command is executed
            columns_values = ", ".join([f"{col} = %s" for col in kwargs])
            print(columns_values)

            # list(kwargs.values()) holds the dictionary values that will be placed in 
            # the place holders %s where column_values are, the [id] will placed into id = %s
            cursor.execute( f"UPDATE {tableName} SET {columns_values} WHERE id = %s;", list(kwargs.values()) + [id])
            self.connection.commit()

py = PostPie('localhost', 'postgres', 'postgres', 'MasterGaming1', 5432)
#py.create_table('bruh', name="VARCHAR(255)", age='INT')
#py.show_table('product')
#py.create_table('product', productName='VARCHAR(255)', price='INT', companyName='VARCHAR(255)', description='TEXT')
#py.insert('product', productName='IPhone', price=999.99, companyName='Apple', description='A phone that is touch phone!')
py.show_custom_table_info('product', 'price', where='price > 100')