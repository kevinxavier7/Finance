from Utils.Tools import validations
from Utils.GeneralTools import run_query, response
import json


@validations
def list_module(event, context):
    
    module = run_query("select * from module", 'get')
    
    if module:
        list_module = []
        for md in module:
            list_module.append(dict(
                module_id = md[0],
                module_name = md[1]
            ))
        return response(200, "list module", list_module)
    
    return response(200, "no module to display", None)


@validations
def create_module(event, context):
    
    data = json.loads(event['body'])
    
    run_query("insert into module(name) values('{}')".format(data['name']), 'post')
    
    return response(200, "module created sucessfully", data)
    
    
    
    
    