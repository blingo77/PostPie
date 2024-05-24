import psycopg2

class PostPie:

    # User must Connect to their PostgreSQL server
    def __init__(self, host_name, db_name, db_user, db_password, db_port):
        self.connection = psycopg2.connect(host=host_name, dbname=db_name, user=db_user, password=db_password, port=db_port)

    def create_table(self, tableName, **kwargs):
        
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

    def show_table(self, tableName):

        """" SHOWS ALL TABLE INFORMATION IN THE TERMINAL """

        cursor = self.connection.cursor()

        cursor.execute(f""" SELECT * FROM {tableName} ;""")

        rows = cursor.fetchall()
        for i in rows:
            print(i)

        cursor.close()
        self.connection.close()

    def show_custom_table_info(self, tableName, *args):

        """" SHOWS TABLE INFORMATION BASED ON *args """

        cursor = self.connection.cursor()

        columns = ", ".join(args)

        cursor.execute(f""" SELECT {columns} FROM {tableName};""")

        rows = cursor.fetchall()

        for i in rows:
            print(i)

        cursor.close()
        self.connection.close()


    def insert(self, tableName, **kwargs):

        cursor = self.connection.cursor()

        columns = ", ".join(kwargs.keys())
        values = ', '.join([f" '{values}'" for values in kwargs.values()])

        cursor.execute(f""" INSERT INTO {tableName} ({columns}) VALUES ({values}); """)

        self.connection.commit()

        cursor.close()
        self.connection.close()

    def delete_row_by_id(self, tableName, id):
        cursor = self.connection.cursor()

        cursor.execute(f""" DELETE FROM {tableName} WHERE id = {id}; """)

        self.connection.commit()

        self.connection.close()
        cursor.close()


    def drop_table(self, tableName):
        cursor = self.connection.cursor()

        cursor.execute(f""" DROP TABLE {tableName}; """)

        self.connection.commit()

        self.connection.close()
        cursor.close()
    
    def get_by_id(self, tableName, id, column):

        """ RETURNS A SINGLE VALUE BASED ON ID AND column"""

        cursor = self.connection.cursor()


        cursor.execute(f""" SELECT  {column} FROM {tableName} WHERE id = {id}; """)

        row = cursor.fetchone()

        cursor.close()
        self.connection.close()

        return row[0]


py = PostPie("localhost", "postgres", "postgres", "MasterGaming1", 5432)
py.create_table('product', name='VARCHAR(255)', price='INT', companyName='VARCHAR(255)')
#py.show_table('products')
