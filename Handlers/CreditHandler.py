from Utils.GeneralTools import run_query, response, response_error
from Utils.Tools import authorized
from Apis.Clients.ClassClient import ValidateClient
import datetime
from dateutil.relativedelta import relativedelta
import json


@authorized
def list_credit(event, context):

    credit = run_query("select c.credit_id, c.client_id, c.credit_value, c.installments, c.term, c.date_credit,\
        c.payment_date, cd.installments_paid, cd.credit_status, cd.balance, c.user_creates\
        from credit c inner join credit_detail cd\
        on c.credit_id = cd.credit_id where cd.credit_status = 'A'", 'get')

    if credit:
        credit_list = []
        
        for cd in credit:
            credit_list.append(dict(
                credit_id=cd[0], client_id=cd[1], credit_value=int(cd[2]), installments=int(cd[3]), term=cd[4], date_credit=str(cd[5]),
                payment_date=cd[6], installments_paid=cd[7], credit_status=cd[8], balance=int(cd[9]), user_creates =cd[10]
            ))
        return response(200, "credit_list", credit_list)

    return response(200, "no credit to display", None)


@authorized
def create_credit(event, context):

    data = json.loads(event['body'])

    client_active = ValidateClient.validate_status(data['client_id'])

    if client_active:

        date = datetime.datetime.now()

        next_payment_date = date + \
            relativedelta(months=1, day=data['payment_date'])

        credit = run_query("insert into credit(client_id, credit_value, installments, term, date_credit, payment_date, user_creates) values(\
            {}, {}, {}, {}, '{}', {}, {})".format(
            data['client_id'], data['credit_value'], data['installments'], data['term'], date, data['payment_date'], event['user_id']), 'post')

        run_query("insert into credit_detail(credit_id, installments_paid, next_payment_date, credit_status, balance, user_creates) values(\
            {}, 0, '{}', 'A', {}, {} )".format(credit, next_payment_date, data['credit_value'], event['user_id']), 'post')

        return response(200, "credit created successfully", data)

    return response_error("inactive or non-existent client")
