from decouple import config
import boto3


def confirmate_cognito(data):

    client = boto3.client('cognito-idp', region_name='us-east-1')
    client.admin_set_user_password(
        UserPoolId="us-east-1_6Hy7SxFvA",
        Username=data['username'],
        Password=data['password'],
        Permanent=True)


def create_user_cognito(data: dict) -> dict:   
  

    client = boto3.client('cognito-idp')
    response = client.admin_create_user(
        UserPoolId="us-east-1_6Hy7SxFvA",
        Username=data['username'],
        UserAttributes=[{"Name": "email", "Value": data['email']}, {
            "Name": "email_verified", "Value": "True"}],
        TemporaryPassword=data['password']
    )

    if response:
       
        confirmate_cognito(data)
        return response


def generate_token(data: dict) -> dict:

    client = boto3.client('cognito-idp', region_name='us-east-1')
    response = client.initiate_auth(
        ClientId=config("COGNITO_USER_CLIENT_ID"),
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": data['username'], "PASSWORD": data['password']})

    return response


def get_username(data):

    client = boto3.client('cognito-idp')
    token = str(data[0]['headers']['Authorization']).replace("Bearer ", "")

    data_user = client.get_user(
        AccessToken=token
    )

    username = data_user['Username']

    return username


    
    