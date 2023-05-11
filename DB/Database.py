import mysql.connector
from decouple import config

def get_connection():
    try:
        connection = mysql.connector.connect(
            db=config('MYSQL_DB'),
            user=config('MYSQL_USER'),
            password=config('MYSQL_PASSWORD'),
            host=config('MYSQL_HOST')
        )
        if connection.is_connected():                   
        
            cursor = connection.cursor()            
            
            return(cursor, connection)            
                            
    except Exception as err:
        print(err)

