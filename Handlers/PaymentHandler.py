from Utils.Tools import authorized
from Utils.GeneralTools import response, run_query, response_error
from Apis.Payments.PaymentClass import ValidatePayment
from datetime import datetime
import json



@authorized
def list_payment(event, context):

    pays = run_query("select * from payments", 'get')

    if pays:
        list_pays = []
        for py in pays:
            list_pays.append(dict(
                pay_id=py[0], credit_id=py[1],pay_value=int(py[2]),
                pay_date=str(py[3], user_creates=py[4])
            ))
        return response(200, "pays list", list_pays)
    
    return response(200, "no payments to display", None)


@authorized
def create_payment(event, context):
    
    data = json.loads(event['body'])
    
    validation_balance = ValidatePayment.validate_balance_credit(data)  
    
    
    if validation_balance[0]:
        
        run_query("insert into payments(credit_id, payment_value, payment_date, user_creates) values({}, {},'{}', {})".format(\
            data['credit_id'], data['payment_value'], data['payment_date'], event['user_id']), 'post')
        
        ValidatePayment.update_credit_detail(data, event)
        
        return response(200, "payment entered sucessfull", data)
    
    return response_error(validation_balance[1])
        
    
    