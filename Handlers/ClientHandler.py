from Utils.Tools import validations, authorized
from Utils.GeneralTools import run_query, response, response_error
import json
from Apis.Clients.ClassClient import UploadS3, ValidateClient
from datetime import datetime


@authorized
def list_client(event, contex):

    data = run_query("select * from client", 'get')

    list_client = []  

    for d in data:
        list_client.append(dict(
            client_id=d[0], document=d[1], email=d[2], name=d[3], last_name=d[4],
            phone=d[5], address=d[7], city=d[8], profession=d[9], user_creates =d[13]
        ))

    return response(200, "Client list", list_client)


@authorized
def create_client(event, context):

    data = json.loads(event['body'])   

    run_query("insert into client(document, email, name, last_name, phone, active, address, city, profession, image, created_at, user_creates) values(\
        {}, '{}', '{}', '{}', '{}', 1, '{}', '{}', '{}', '{}', '{}', {})".format(
        data['document'], data['email'], data['name'], data['last_name'], data['phone'], data['address'], data['city'], data['profession'],
        '/bucket-images-profile/img{}.jpeg'.format(data['name']), datetime.now(), event['user_id']), 'post')

    UploadS3.upload_image(data['image'], data['name'])

    return response(201, "client created successfully", data)


@authorized
def update_client(event, context):

    parameters = event['pathParameters']       

    client = ValidateClient.validate_status(parameters['client_id'])

    if client:
        data = json.loads(event['body'])

        run_query("update client set email ='{}', name ='{}', last_name ='{}', phone ='{}', city ={}, profession ='{}', image ='{}', updated_at = '{}' where client_id = {}".format(
            data['email'], data['name'], data['last_name'], data['phone'], data['city'], data['profession'], data['image'], datetime.now(), parameters['client_id']), 'post')

        return response(200, "client updated sucessfully", data)

    return response_error("user does not exist")


@validations
def create_city(event, context):

    data = json.loads(event['body'])

    run_query("insert into city(cod_city, name) values({}, '{}')".format(
        data['cod_city'], data['name']), 'post')

    return response(200, "city created sucessfully", data)
