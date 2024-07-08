
from postpie import PostPie
from connection import pool

connection.connect(config=config)

def get_data_from_database():
    with pool.getconn() as conn:  # Get a connection from the pool
        with conn.cursor() as cur:  # Create a cursor object
            cur.execute("SELECT * FROM customer")
            return cur.fetchall()
    
data = get_data_from_database()

print(data)