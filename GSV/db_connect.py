import psycopg2
from psycopg2 import OperationalError
import configparser

def connect_to_database():
    config = configparser.ConfigParser()
    config.read('config.ini')

    dbname = config['database']['dbname']
    user = config['database']['user']
    password = config['database']['password']
    host = config['database']['host']

    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        print("Database running well")  # we should remove this line in the future
        return connection
    except OperationalError as e:
        print(f"Error in connecting with database: {e}")
        return None





