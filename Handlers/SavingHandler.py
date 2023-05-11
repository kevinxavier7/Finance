from Utils.Tools import validations, authorized
from Utils.GeneralTools import run_query, response, response_error
import json
from Apis.Clients.ClassClient import ValidateClient

@authorized
def list_saving(event, contex):

    data = run_query("select * from savings_account", 'get')

    list_client = []
    for d in data:
        list_client.append(dict(
            account_id=d[0], client_id=d[1], account_number=d[2], balance=int(d[3]), activation_date=str(d[4]),
            city_id=d[5], country_id=d[6], account_status=d[7], user_creates=d[8]
        ))

    return response(200, "savings_account list", list_client)


@authorized
def create_saving(event, context):   

    data = json.loads(event['body'])
    
    client_active = ValidateClient.validate_status(data['client_id'])
    
    if client_active:       

        run_query("insert into savings_account(client_id, account_number, balance, activation_date, city_id, country_id, account_status, user_creates) values(\
            {}, '{}', {}, now(), {}, {}, 1, {})".format(data['client_id'], data['account_number'], data['balance'], data['city_id'], data['country_id'], event['user_id']), 'post')

        return response(201, "savings account created successfully", data)
    
    return response_error("inactive or non-existent client")


@authorized
def update_saving(event, context):

    data = json.loads(event['body'])

    run_query("update savings_account set balance ={}, account_status = {} where account_id ={}".format(
        data['balance'], data['account_status'], data['account_id']), 'post')

    return response(200, "saving account updated sucessfully", data)


@validations
def create_country(event, context):

    data = json.loads(event['body'])

    run_query("insert into country(cod_country, name) values({}, '{}')".format(
        data['cod_country'], data['name']), 'post')

    return response(200, "country created sucessfully", data)
