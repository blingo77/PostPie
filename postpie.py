import psycopg2

class PostPie:

    # User must Connect to their PostgreSQL server
    def __init__(self, host_name, db_name, db_user, db_password, db_port):
        self.connection = psycopg2.connect(host=host_name, dbname=db_name, user=db_user, password=db_password, port=db_port)
        

    def create_table(self):
        pass

    def show_table(self, tableName):
        cursor = self.connection.cursor()

        cursor.execute(f""" SELECT * FROM person """)

        rows = cursor.fetchall()
        for i in rows:
            print(i)


        cursor.close()
        self.connection.close()

