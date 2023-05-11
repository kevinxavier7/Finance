import json
from Utils.Tools import validations, authorized
from Utils.GeneralTools import run_query, response, response_error
from Apis.Users.UserClass import ValidateUser, validate_fields_input
from jwt import encode
from decouple import config
from Utils.AuthTools import create_user_cognito
from datetime import datetime


@authorized
def list_user(event, context): 
          
    sql = "select user_id, username, email, name, last_name, active from users where active = 1"
    data = run_query(sql, "get")   
    
    if data:
        list_user = []
        for d in data:
            list_user.append(dict(
                user_id=d[0],
                username=d[1],
                email=d[2],
                name=d[3],
                last_name=d[4],
                active=d[5]
            ))
        return response(200, "user list", list_user)
    
    return response(200, "no user to display", None)



def create_user(event, context):   
    
    data = json.loads(event['body'])         

    validate_input = validate_fields_input.validate_created_user(data)

    if validate_input[0]:      

        validated_email = ValidateUser.validate_email(data['email'])

        if validated_email:

            email_exist = ValidateUser.validate_new_email(data['email'])

            if email_exist:

                return response_error("this email already exists")

            else:                                                                                           
                                        
                new_password = encode({'key': data['password']}, config("SECRET"), algorithm="HS256" )
                sql = "insert into users(document, username, email, password, name, last_name, age, phone, active, created_at)\
                    values({},'{}','{}','{}','{}','{}',{}, '{}', 1, '{}')".format(\
                    data['document'], data['username'], data['email'], new_password, data['name'], data['last_name'], data['age'], data['phone'], datetime.now())
                
                try:                    
                    create_user_cognito(data)
                    run_query(sql, 'post') 
                    return response(201, "user created successfully", data)
                
                except Exception as err:
                    return response_error(str(err))                           
                           
        return response_error("error, validate email")

    return response_error("the {} field cannot be empty".format(validate_input[1]))
    

@authorized
def update_user(event, context):    
  
    parameters = event['pathParameters']
    data = json.loads(event['body'])     

    user_exist = ValidateUser.validate_existence(parameters['user_id'])

    if user_exist:

        validate_input = validate_fields_input.validate_update_user(data)

        if validate_input[0]:
            validated_email = ValidateUser.validate_email(data['email'])
            if validated_email:
                sql = "update users set email ='{}', name ='{}', last_name ='{}', age = {}, phone = {}, updated_at = '{}' where user_id = {}".format(
                    data['email'], data['name'], data['last_name'], data['age'], data['phone'], datetime.now(), parameters['user_id']
                )               
                run_query(sql, 'post')

                return response(200, "user updated successfully", {
                    "parameters": parameters['user_id'],
                    "data": data
                })                

            return response_error("error, validate email")

        return response_error("the {} field cannot be empty".format(validate_input[1]))

    return response_error("user: {} not exist".format(parameters['user_id']))
    
   




    
    
    

