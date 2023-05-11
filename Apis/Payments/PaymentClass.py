from Utils.GeneralTools import run_query, response_error
import datetime
from dateutil.relativedelta import relativedelta


class ValidatePayment():

    def validate_balance_credit(data):

        credit = run_query("select credit_id, balance, credit_status from credit_detail where credit_id = {}".format(
            data['credit_id']), 'get')
        
        if credit == []:
            return (False, "this credit does not exist")
        elif credit[0][2] == 'P':
            return (False, "the credit is already canceled")
        elif credit[0][1] < data['payment_value']:
            return (False, "the credit balance is less than the payment to be made")
        else:
            return (True,)

    def get_detail_credit(data: dict) -> dict:

        credit = run_query("select c.credit_id, max(p.payment_id),c.payment_date, p.payment_date as last_date_payment, c.installments, cd.installments_paid, cd.balance\
            from payments p \
            inner join credit c on c.credit_id = p.credit_id\
            inner join credit_detail cd on c.credit_id = cd.credit_id\
            where c.credit_id = {}".format(
            data['credit_id']), 'get')

        return credit

    def update_credit_detail(data: dict, event: dict) -> dict:

        credit = ValidatePayment.get_detail_credit(data)

        if credit == []:
            return False
        else:

            installments = int(data['payment_value'] / credit[0][4])
            installments_paid = credit[0][5] + installments

            current_date = datetime.datetime.strptime(
                data['payment_date'], '%Y-%m-%d')

            balance = credit[0][6] - data['payment_value']
            if balance == 0:
                status = 'P'
                next_payment_date = ""

            else:
                status = 'A'
                next_payment_date = current_date + \
                    relativedelta(months=1, day=credit[0][2])

            run_query("update credit_detail set installments_paid = {}, next_payment_date = '{}', balance = {}, credit_status ='{}', last_payment_date = '{}', user_creates = {} where credit_id ={}".format(
                installments_paid, next_payment_date, balance, status, data['payment_date'], event['user_id'], data['credit_id']), 'post')
