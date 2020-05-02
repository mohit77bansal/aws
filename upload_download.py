# from boto.s3.key import Key
import boto3
import os
import shutil

RESOUCE_NAME = ""
RESOURCE_PARENT_PATH = "."
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_KEY =  os.getenv("AWS_SECRET_ACCESS_KEY", "")
RESOURCE_BUCKET_NAME = os.getenv("BUCKET_NAME", "")
RESOURCE_UPLOAD_VERSION = os.getenv("RESOURCE_UPLOAD_VERSION", "")
RESOURCE_DOWNLOAD_VERSION = os.getenv("RESOURCE_UPLOAD_VERSION", "")

def upload_resource(resource_type, upload_from):
    client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    new_version = RESOURCE_UPLOAD_VERSION
    print("latest version to be uploaded", new_version)
    for subdir, dirs, files in os.walk(upload_from):
        print(subdir,dirs,files)
        for file in files:
            fullpath = os.path.join(subdir, file)
            key_bucket = os.path.join(resource_type,new_version,os.path.basename(upload_from), fullpath[len(upload_from) + 1:])
            print("Uploading File:", fullpath,key_bucket)
            response = client.upload_file(Bucket=RESOURCE_BUCKET_NAME, Filename=fullpath, Key=key_bucket)


def download_dir(client, resource, dist, local, bucket):
    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_dir(client, resource, subdir.get('Prefix'), local, bucket)
        for file in result.get('Contents', []):
            dest_pathname = os.path.join(local, file.get('Key').split("resources/")[1])
            print ("dest_pathname", dest_pathname)
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            resource.meta.client.download_file(bucket, file.get('Key'), dest_pathname)

def download_resources():
    resource_type = RESOUCE_NAME
    download_to = RESOURCE_PARENT_PATH
    client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
    resource = boto3.resource('s3')

    download_version = RESOURCE_DOWNLOAD_VERSION
    print ("version to be downloaded", download_version)
    download_from = resource_type+"/"+download_version

    download_dir(client, resource, download_from, download_to, RESOURCE_BUCKET_NAME)


if __name__ == "__main__":
    upload_resource(RESOUCE_NAME, RESOURCE_PARENT_PATH)








