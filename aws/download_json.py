import boto3
from config.environment import settings
import os
session = boto3.Session(aws_access_key_id=settings.aws_access_key_id, aws_secret_access_key=settings.aws_secret_access_key, region_name=settings.aws_region)




def download_all_jsons():
    s3 = session.resource('s3')
    bucket = s3.Bucket('altinfo-crimecheck')
    for s3_object in bucket.objects.all():
        path, filename = os.path.split(s3_object.key)
        path = f'{settings.base_data_path}/{path}'
        if not os.path.isdir(path):
            os.makedirs(path)
        if not os.path.isfile(f'{path}/{filename}'):
            print(f'downloading file = {filename}')
            bucket.download_file(s3_object.key, f'{path}/{filename}')


