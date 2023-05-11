from Utils.GeneralTools import run_query


class NewBalance():
    
    
    def get_balance(data):
        
        value = run_query(
                "select balance from savings_account where account_id = {}".format(data['account_id']), 'get')
        
        balance = value[0][0]
        
        if data['transaction_value'] > balance:
            
            return (False, )
        
        return (True, balance)
    
    
    def insert_balance(data):
        
        balance = NewBalance.get_balance(data)      
       

        if str(data['transaction_status']).upper() == 'A':       

           
            run_query("update savings_account set balance = {} where account_id = {} and client_id = {}".format(
                balance[1] - data['transaction_value'], data['account_id'], data['client_id']), 'post')

    
    