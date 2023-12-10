import requests
from requests_toolbelt import MultipartEncoder
import json
import time
from pathlib import Path
import os
from dotenv import load_dotenv
#from gallery.models import Image
#from client.models import Client, Project

current_dir = Path(__file__).resolve().parent
ven = current_dir / "../.env"
load_dotenv(ven)


load_dotenv()
api_key = os.getenv('API_KEY')
user_email = os.getenv('USER_EMAIL')
account_ID = os.getenv('ACCOUNT_ID')

class Encode_Metadata:
    def __init__(self, *args):
        self.formated_meta = args



    def direct_request_encoder(self):

        mutipart_data = MultipartEncoder(fields={
            'metadata': json.dumps(self.formated_meta),
            'requireSignedURLs': 'false'

        })
        return mutipart_data

    def upload_request_encoder(self, img_file):
        mutipart_data = MultipartEncoder(fields={
            'metadata': json.dumps(self.formated_meta),
            'requireSignedURLs': 'false',
            'file': (img_file, open(img_file, 'rb'), 'image/jpeg')
        })
        return mutipart_data

class APICall:

    def __int__(self):
        super().__init__()
        
    def get_batch_token(self):
        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1/batch_token'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
            'X-Auth-Email': user_email
        }
        response = requests.get(url, headers=headers)
        cloudflare_token = response.json()["result"]["token"]
        print(cloudflare_token)
        return cloudflare_token

    def auth_direct_upload(self, encoded_data, ):
        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v2/direct_upload'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': encoded_data.content_type,
            'X-Auth-Email': user_email
        }
        response = requests.post(url, headers=headers, data=encoded_data)
        
        if response.json()["result"]["id"]:
            cloudflare_id = response.json()["result"]["id"]
            
            return str(cloudflare_id)
        else:
            
            return 'error', response

    def get_batch_urls(self, encoded_data, token):

        url = f'https://batch.imagedelivery.net/images/v2/direct_upload?result=3'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-type': encoded_data.content_type,
            'X-Auth-Email': user_email
            
        }

        response = requests.post(url, headers=headers, data=encoded_data)
        cloudflare_id = response.json()
        
        return cloudflare_id

    def back_end_upoload(self, meta_passed, img_file):
        print('made it')
        title, author, meta_tag, client, category, private, group = meta_passed
        metadata_packed = {
            'title': title,
            'author': author,
            'meta_tag': meta_tag,
            'client': client,
            'category': category,
            'group': group
        }
        print('encoding')
        # when encoding a mulitpart/form-data

        encoded_data = MultipartEncoder(fields={
            'metadata': json.dumps(metadata_packed),
            'requireSignedURLs': 'false',
            'file': (img_file, open(img_file, 'rb'), 'image/jpeg')

        })
        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': encoded_data.content_type,
            'X-Auth-Email': user_email
        }

        print('responding')
        time.sleep(10)
        response = requests.post(url, headers=headers, data=encoded_data)
        print(response.text)


    def get_image_usage(self, meta_passed):
        pass

    def delete_image(self, cloudflare_id):

        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1/{cloudflare_id}'

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
            'X-Auth-Email': user_email
        }
        time.sleep(.02)
        response = requests.delete(url, headers=headers)
        print(response.text)

    def image_details(self, cloudflare_id):

        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1/{cloudflare_id}'

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
            'X-Auth-Email': user_email
        }
        time.sleep(15)
        response = requests.get(url, headers=headers)
        print(response.text)

    def image_download(self, cloudflare_id):

        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1/{cloudflare_id}/blob'

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
            'X-Auth-Email': user_email
        }
        time.sleep(15)
        response = requests.get(url, headers=headers)
        print(response.text)

    def image_update(self, meta_passed, cloudflare_id):
        print(cloudflare_id)

        metadata_packed = { 
                        'title': str(meta_passed.get('title')),
                        'tag': str(meta_passed.get('tag')),
                        'display': str(meta_passed.get('display')),
                        'client_id': str(meta_passed.get('client_id')),
                        'project_id': str(meta_passed.get('project_id')), 
                        'silk_id': str(meta_passed.get('silk_id'))
        }
            


        url = f"https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1/{cloudflare_id}"
        

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
            'X-Auth-Email': user_email
        }
        data = {
            'filename': meta_passed.get('title'),
            'metadata': metadata_packed,
            'requireSignedURLs': False
        }
        time.sleep(.02)
        response = requests.patch(url, headers=headers, json=data)
        if response.json()["success"] == True:
            cloudflare_id = response.json()["result"]["id"]
            
            return 'success'
        else:
            return 'error', response
    # Backend Oberations
    # this function can be used to import a large set of images that already exits in the CDN. Ideally for the initial migration to the site/app     
"""    def mass_import(self):

        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1'

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
            'X-Auth-Email': user_email
        }

        params = {
            'page': 3,
            'per_page': 50
        }
        image_list = []
        response = requests.get(url, headers=headers, params=params)
        data_packets = response.json()
        results = data_packets['result']
        images = results['images']    
        for image in images:
            imageid = image['id'] 
            filename = image['filename']
            variants = image['variants']
            uploaded = image['uploaded']
            #meta = image['meta']
            #print(meta) #meta 
            for instance in variants:
                if 'display' in instance:
                    image_linked = instance
            client = Client.objects.get(name='Soft Subversion')        
            project = Project.objects.get(name='Soft Subversion') 
            Image.objects.create(
                title=filename,
                date=uploaded,
                tag='site_image',
                display='familygal',
                client_id=client,
                project_id=project,
                image_link=image_linked,
                cloudflare_id=imageid
            )"""
        
