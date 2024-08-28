# -*- coding: utf-8 -*-
import boto3
import json
import logging
from botocore.exceptions import ClientError

# Function to search for credentials in Secrets Manager
def get_secret():
    secret_name = "rds/credentials/desafioML"  # Name of your secret
    region_name = "us-east-1"  # AWS Secrets Manager Region

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except ClientError as e:
        logging.error(f"Error getting secret: {e}")
        return None

# Function to download a file from S3
def download_file_from_s3(bucket_name, file_key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    return obj['Body'].read().decode('utf-8')
