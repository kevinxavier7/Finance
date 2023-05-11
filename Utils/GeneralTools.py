from DB.Database import get_connection
import json


def run_query(sql, tipo):

    cox = get_connection()
    cursor = cox[0]
    connection = cox[1]

    cursor.execute(sql)

    if tipo == 'get':
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    elif tipo == 'post':
        connection.commit()
        fk = cursor.lastrowid
        cursor.close()
        connection.close() 
        return fk  
        
       
        
def response(statuscode, response, content):

    return {
        'statusCode': statuscode,
        'body': json.dumps({
            'message': response,
            'content': content
        })
    }

def response_error(response):
    
    return {
        'statusCode': 400,
        'body': json.dumps({
            'error': response,
            
        })
    }
    

def get_user_id(username):
    user = run_query("select user_id from users where username = '{}'".format(username), 'get')   
    
    user_id = user[0][0]    
    
    return user_id