import requests
from requests_toolbelt import MultipartEncoder
import json
import time
from pathlib import Path
import os
from dotenv import load_dotenv
from gallery.models import Image
from client.models import Client, Project

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

    def auth_direct_upload(self, encoded_data, ):
        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v2/direct_upload'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': encoded_data.content_type,
            'X-Auth-Email': user_email
        }
        response = requests.post(url, headers=headers, data=encoded_data)
        print(response.text)
        cloudflare_id = response.json()["result"]["id"]
        print('id ', cloudflare_id)
        return cloudflare_id

    def front_end_upoload(self, encoded_data, cloudflare_id, metadata, img_file):

        url = f'https://upload.imagedelivery.net/4_y5kVkw2ENjgzV454LjcQ/{cloudflare_id}'
        print(url)
        meta_list = metadata
        headers = {
            'Content-type': encoded_data.content_type,
        }
        response = requests.post(url, headers=headers, data=meta_list)
        print(response.text)

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
        time.sleep(15)
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
        ''
        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1/{cloudflare_id}/blob'

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
            'X-Auth-Email': user_email
        }
        time.sleep(15)
        response = requests.get(url, headers=headers)
        print(response.text)

    def image_update(self, meta_passed, cloudflare_id, type_image):
        print(meta_passed, cloudflare_id)
        if type_image == 'image':
            title, tag, private, display, aspect, client_id, project_id, cloudflare_id, silk_id  = meta_passed

            metadata_packed = { 
                            'title': title,
                            'tag': tag,
                            'private': private,
                            'display': display,
                            'aspect': aspect,
                            'client_id': client_id,
                            'project_id': project_id, 
                            'cloudflare_id': cloudflare_id, 
                            'silk_id': silk_id

            }
            
            
        elif type_image == 'print':
            title, cost, details, status, display, aspect, cloudflare_id, silk_id  = meta_passed
            cost = str(cost)
            metadata_packed = { 
                            'title': title,
                            'cost': cost,
                            'details': details,
                            'status': status,
                            'display': display,
                            'aspect': aspect,
                            'cloudflare_id': cloudflare_id, 
                            'silk_id': silk_id

            }
            private = status

        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1/{cloudflare_id}'
        print(url)

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
            'X-Auth-Email': user_email
        }
        data = {
            'filename': title,
            'metadata': metadata_packed,
            'requireSignedURLs': private
        }
        time.sleep(15)
        response = requests.patch(url, headers=headers, json=data)
        print(response.text)
    # Backend Oberations
    # this function can be used to import a large set of images that already exits in the CDN. Ideally for the initial migration to the site/app     
    def mass_import(self):

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
            )
        
