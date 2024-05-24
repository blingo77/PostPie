import psycopg2

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

        cursor = self.connection.cursor()

        columns = ', '.join(args)

        cursor.execute(f""" SELECT {columns} FROM {tableName} WHERE id = {id}; """)

        values = cursor.fetchone()

        cursor.close()
        self.connection.close()

        return list(values)

  


py = PostPie("localhost", "postgres", "postgres", "MasterGaming1", 5432)
#py.create_table('product', name='VARCHAR(255)', price='INT', companyName='VARCHAR(255)')
#py.insert('product', name='IPhone 15', price=1000, companyName='Apple')
#py.insert('product', price=500, name='LapTop', companyName='HP')
#py.show_table('product')
#py.show_custom_table_info('product', 'name', 'price')
#price = py.get_by_id('product', 1, 'price')
#print(price)
print(py.get_row_by_id('product', 1, '*'))