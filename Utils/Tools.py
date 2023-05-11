from Apis.Users.UserModel import BaseUser
from Apis.Auth.AuthModel import BaseAuth
from Apis.Clients.ClientModel import BaseClient
from Apis.Savings.SavingModel import BaseSaving
from Apis.Transactions.TransactionModel import BaseTransaction
from Apis.Credits.CreditModel import BaseCredit
from Apis.Payments.PaymentModel import BasePayment
from sqlalchemy import create_engine
from decouple import config
import json
from Apis.Auth.ListLambda import list
from Utils.AuthTools import get_username
from Apis.Auth.AuthClass import ValidateAuth
from .GeneralTools import response
from .GeneralTools import get_user_id


def validations(validate):

    def wrapper(*args, **kwargs):

        data = args

        try:
            username = get_username(data)
            if username:
                result = validate(*args, **kwargs)
                return result

            return response(400, "invalid or expired token", None)

        except Exception as err:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': str(err)
                })
            }
    return wrapper


def authorized(validations):

    def wrapper(*args, **kwargs):

        data = args
        try:            
            username = get_username(data)
            user_id = get_user_id(username)
            data[0]['user_id']= user_id          

            if data[0]['resource'] in list:                

                user_permission = ValidateAuth.validate_permission(
                    username, list[data[0]['resource']])

                if user_permission:
                    result = validations(*args, **kwargs)
                    return result
                return response(400, "You do not have permission to access this module", None)

        except Exception as err:

            return response(400, str(err), None)

    return wrapper


# build tables


def create_tables(event, context):

    engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(config('MYSQL_USER'),
                                                                config('MYSQL_PASSWORD'), config('MYSQL_HOST'), config('MYSQL_DB')))

    table_base = (BaseUser, BaseAuth, BaseClient, BaseSaving, BaseTransaction, BaseCredit, BasePayment)

    for tb in table_base:
        tb.metadata.create_all(engine)

    return response(200, "tables created sucessfull", None)
