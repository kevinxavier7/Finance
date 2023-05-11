import boto3
import base64
from Utils.GeneralTools import run_query


class UploadS3():
    
    def upload_image(image, user): 
        
        photo = base64.b64decode(image)
        
        s3_resource = boto3.resource('s3')
        
        file_name = 'img{}.png'.format(user)
        
        s3_resource.Bucket('bucket-images-profile').put_object(Key=file_name, Body=photo)        
 
       
class ValidateClient():
    
    def validate_status(client):
        
        client_active = run_query("select client_id from client where active = 1 and client_id = {} ".format(client), 'get')      
        
        if client_active == []:
            return False
        return True
               
   
        
    

        