# -*- coding: utf-8 -*-
import boto3
import json
import logging
from botocore.exceptions import ClientError

# Função para buscar credenciais no Secrets Manager
def get_secret():
    secret_name = "rds/credentials/desafioML"  # Nome do seu segredo
    region_name = "us-east-1"  # Região do AWS Secrets Manager

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)
    except ClientError as e:
        logging.error(f"Erro ao obter segredo: {e}")
        return None

# Função para baixar um arquivo do S3
def download_file_from_s3(bucket_name, file_key):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    return obj['Body'].read().decode('utf-8')
