import psycopg2

# A PostgreSQL table must be created already to use

class PostPie:

    # User must Connect to their PostgreSQL server
    def __init__(self, host_name, db_name, db_user, db_password, db_port):
        self.connection = psycopg2.connect(host=host_name, dbname=db_name, user=db_user, password=db_password, port=db_port)

    def create_table(self, tableName, **kwargs):
        cursor = self.connection.cursor()

        columnNames = ", ".join(kwargs.keys())
        columValues = ', '.join([f" {values}" for values in kwargs.values()])

        cursor.execute(f""" CREATE TABLE IF NOT EXISTS "{tableName}" ( id SERIAL PRIMARY KEY, {columnNames} {columValues}); """)

        self.connection.commit()

        cursor.close()
        self.connection.close()

    def show_table(self, tableName, **kwargs):
        cursor = self.connection.cursor()

        cursor.execute(f""" SELECT * FROM {tableName} ;""")

        rows = cursor.fetchall()
        for i in rows:
            print(i)


        cursor.close()
        self.connection.close()

    def insert(self, tableName, **kwargs):
        cursor = self.connection.cursor()

        columns = ", ".join(kwargs.keys())
        values = ', '.join([f" '{values}'" for values in kwargs.values()])

        print(f""" INSERT INTO {tableName} ({columns}) VALUES ({values}); """)

        cursor.execute(f""" INSERT INTO {tableName} ({columns}) VALUES ({values}); """)

        self.connection.commit()

        cursor.close()
        self.connection.close()


