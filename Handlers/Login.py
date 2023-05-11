from Utils.GeneralTools import response, response_error
import json
from Utils.AuthTools import generate_token


def login(event, context):

    data = json.loads(event['body'])       
            
    try:                
        token = generate_token(data)               

        return {
            'statusCode':200,
            'body': json.dumps({
                'message': "login successfull",
                'token': token
            })
        }
    except Exception as err:
        return response_error(str(err))
            
        

   