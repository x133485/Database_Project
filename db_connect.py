import psycopg2
from psycopg2 import OperationalError

def connect_to_database():
    try:
        connection = psycopg2.connect(
            dbname='database_Project',  
            user='postgres',            
            password='1985',          
            host='localhost'            
        )
        print("Database running well") #we should remove this line in the future
        return connection
    except OperationalError as e:
        print(f"Error in connecting with database: {e}")
        return None





