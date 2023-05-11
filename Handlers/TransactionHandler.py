from Utils.Tools import authorized
from Utils.GeneralTools import run_query, response, response_error
import json
from Apis.Transactions.TransacctionClasess import NewBalance
from datetime import datetime


@authorized
def list_transaction(event, contex):

    data = run_query("select * from transaction", 'get')   
    
    if data:
        list_transaction = []
        for d in data:           
            list_transaction.append(dict(
                transaction_id=d[0],account_id=d[1], cliente_id=d[2],               
                current_balance=int(d[3]), ending_balance=str(d[4]),
                transaction_status=d[5], user_creates=d[6]
                
                
            ))
        return response(200, "transaction list", list_transaction)
    
    return response(200, "no user to display", None)


@authorized
def create_transaction(event, context):   
    
    data = json.loads(event['body'])
    
    validate_balance = NewBalance.get_balance(data)
    
    if validate_balance[0]:        

        run_query("insert into transaction(account_id, client_id, transaction_value, date_transaction, transaction_status, user_creates) values(\
            {}, {}, {}, '{}', '{}', {} )".format(data['account_id'], data['client_id'], data['transaction_value'], datetime.now(),
                                            data['transaction_status'], event['user_id']), 'post')

        NewBalance.insert_balance(data)

        return response(200, "transaction created sucessfully", data)

    return response_error("you don't have enough balance")