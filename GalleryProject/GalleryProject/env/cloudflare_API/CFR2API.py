import boto3
from pathlib import Path
import os
from dotenv import load_dotenv

class CloudflareR2API:
    
    def __int__(self):
        current_dir = Path(__file__).resolve().parent		
        ven = current_dir / "../.env"
        load_dotenv(ven)
        load_dotenv()
        
        self.CFR2_TOKEN = os.getenv('CFR2_TOKEN')
        self.CFR2_ACC_ID = os.getenv('CFR2_ACC_ID')
        self.CFR2_ACC_KEY = os.getenv('CFR2_ACC_KEY')
        self.CFR2_ENDPOINT = os.getenv('CFR2_ENDPOINT')
        self.CFR2_BUCKET = os.getenv('CFR2_BUCKET')


        self.s3 = boto3.client(
            's3',
            aws_access_key_id=self.CFR2_ACC_ID,
            aws_secret_access_key=self.CFR2_ACC_KEY,
            endpoint_url=self.CFR2_ENDPOINTs
        )

    # Upload a Document:
    def upload_r2_object(self, object_name, file_path):

        headers = {'x-amz-meta-key1': 'value1', 'x-amz-meta-key2': 'value2'}
        self.s3.upload_file(file_path, self.bucket_name, object_name, ExtraArgs={'Metadata': headers})

    # Download a Document:
    def download_r2_object(self, object_name, download_path):

        self.s3.download_file(self.bucket_name, object_name, download_path)

    # Update (Put) a Document:
    def update_r2_object(self, object_name, file_path):
        self.upload_r2_object(object_name, file_path) 

    # Delete a Document:
    def delete_r2_object(self, object_name):

        self.s3.delete_object(Bucket=self.bucket_name, Key=object_name)

    # Generate Presigned URL:
    def generate_presigned_url(self, object_name, expiration=3600):

        url = self.s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': object_name},
            ExpiresIn=expiration
        )
        return url


