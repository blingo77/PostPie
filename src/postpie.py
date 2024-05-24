# %s is only a place holder for column values, not column names

import psycopg2
import sqlalchemy

class PostPie:

    # User must Connect to their PostgreSQL server
    def __init__(self, host_name, db_name, db_user, db_password, db_port):
        self.connection = psycopg2.connect(host=host_name, dbname=db_name, user=db_user, password=db_password, port=db_port)

    def create_table(self, tableName: str, **kwargs):
        
        """" CREATES A TABLE IF IT DOSENT EXIST ALREADY """

        cursor = self.connection.cursor()

        columnNames = " ".join(kwargs.keys())
        columnValues = ' '.join([f" {values}" for values in kwargs.values()])

        columnNames = columnNames.split()
        columnValues = columnValues.split()

        sqlComand = ''

        for i in range(len(columnNames)):
            sqlComand += columnNames[i] + " " + columnValues[i] + ' , '

        sqlComand = sqlComand.split()
        sqlComand[-1] = ''
        sqlComand = ' '.join(sqlComand)

        cursor.execute(f""" CREATE TABLE IF NOT EXISTS {tableName} ( id SERIAL PRIMARY KEY, {sqlComand} ); """)

        self.connection.commit()

        cursor.close()
        self.connection.close()

    def show_table(self, tableName : str):

        """" SHOWS ALL TABLE INFORMATION IN THE TERMINAL """

        cursor = self.connection.cursor()

        cursor.execute(f""" SELECT * FROM {tableName} ;""")

        rows = cursor.fetchall()
        for i in rows:
            print(i)

        cursor.close()
        self.connection.close()

    def show_custom_table_info(self, tableName : str, *args):

        """" SHOWS TABLE INFORMATION BASED ON *args """

        cursor = self.connection.cursor()

        columns = ", ".join(args)

        cursor.execute(f""" SELECT {columns} FROM {tableName};""")

        rows = cursor.fetchall()

        for i in rows:
            print(i)

        cursor.close()
        self.connection.close()


    def insert(self, tableName : str, **kwargs):

        cursor = self.connection.cursor()

        columns = ", ".join(kwargs.keys())
        values = ', '.join([f" '{values}'" for values in kwargs.values()])

        cursor.execute(f""" INSERT INTO {tableName} ({columns}) VALUES ({values}); """)

        self.connection.commit()

        cursor.close()
        self.connection.close()

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
    
    def get_row_by_id(self, tableName : str, id : int,  *args) -> list:

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
