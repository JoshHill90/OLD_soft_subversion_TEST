from gallery.models import Image
from client.models import Client, Invite, Project
from django.db.models import Q
from django.contrib.auth.models import User
from pathlib import Path
import os
import json
from django.conf import settings

class DataSetUpdate ():
    def __init__(self):
        super().__init__()
    
    
    def clientJsonData(self, jsonDataSets):
        json_filename = 'clientData.json'
        
        for static_dir in settings.STATICFILES_DIRS:
            json_path = os.path.join(static_dir, 'json', json_filename)
            json_directory = os.path.dirname(json_path)
            Path(json_directory).mkdir(parents=True, exist_ok=True)
        with open(json_path, "w") as json_writer:
            json.dump(jsonDataSets, json_writer) 
            
    def invoiceDetailsJson(self, jsonDataSets):
        json_filename = 'invoiceDetails.json'
        for static_dir in settings.STATICFILES_DIRS:
            json_path = os.path.join(static_dir, 'json', json_filename)
            json_directory = os.path.dirname(json_path)
            Path(json_directory).mkdir(parents=True, exist_ok=True)
        with open(json_path, "w") as json_writer:
            json.dump(jsonDataSets, json_writer) 
    
    def NameListJson(self, jsonDataSets):
        json_filename = 'NameList.json'
        for static_dir in settings.STATICFILES_DIRS:
            json_path = os.path.join(static_dir, 'json', json_filename)
            json_directory = os.path.dirname(json_path)
            Path(json_directory).mkdir(parents=True, exist_ok=True)
        with open(json_path, "w") as json_writer:
            json.dump(jsonDataSets, json_writer) 
    
    
    
    def json_chart_data(self):
        jsonDataSets = []
        image_list = Image.objects.all()
        project_list = Project.objects.all()
        client_list = Client.objects.exclude(Q(id="1"))

        site_image = Image.objects.filter(Q(project_id__name="Soft Subversion"))
        client_images = Image.objects.exclude(Q(project_id__name="Soft Subversion"))
        client_images_list = {}
        site_image_count = len(site_image)
        client_image_count = len(client_images)

        image_list_count = len(image_list)
        site_Image_data = {'siteImageCount': site_image_count}
        client_Image_data = {'clientImageCount': client_image_count}
        total_Image_data = {'totalImageCount': image_list_count}
        for client in client_list:
            client_images_count = 0
            for image in image_list:
                if image.client_id == client:
                    client_images_count +=1
                    client_images_list[client.id] = {
                        "clientsName": client.name,
                        "clientsCount": client_images_count
                        }
                    
                    jsonDataSets = {
                        'clientImageList': client_images_list,
                        'site_Image_data': site_Image_data,
                        'client_Image_data': client_Image_data,
                        'total_Image_data': total_Image_data
                        }

        

        self.clientJsonData(jsonDataSets)

		# setting up JSON string 

    def json_user_list_check(self):
        username_list = []
        code_list = []
        email_list = []
        
        users = User.objects.all()
        invite_code = Invite.objects.filter(used=False)
        
        for user_name in users:
            username_list.append(user_name.username)
            email_list.append(user_name.email)
        for code in invite_code:
            code_list.append(code.hexkey)
        name_list = {'name_list':username_list}
        code_check = {'code_list': code_list}
        user_email = {'email_list': email_list}
        json_list = [name_list, code_check, user_email]
        self.NameListJson(json_list)

        
