from Utils.Tools import validations
from Utils.GeneralTools import response
import json
from Apis.Auth.AuthClass import ValidateAuth


@validations
def assign_permission(event, context):
    
    data = json.loads(event['body'])   
    
    ValidateAuth.insert_permission(data['user_id'], data['module_list'],data)   
    
    return response(200, "permission assigned successfully", data)                              
   
     
        
    
    