# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import ClientError
import logging
import time

# Configuração de logging
logging.basicConfig(
    filename='email_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Função para enviar e-mails um por vez
def send_emails(sender_email, recipient_emails, subject, body_text):
    ses = boto3.client('ses', region_name='us-east-1')

    for recipient_email in recipient_emails:
        try:
            response = ses.send_email(
                Source=sender_email,
                Destination={
                    'ToAddresses': [recipient_email]
                },
                Message={
                    'Subject': {
                        'Data': subject
                    },
                    'Body': {
                        'Text': {
                            'Data': body_text
                        }
                    }
                }
            )
            message_id = response['MessageId']
            logging.info(f"E-mail enviado com sucesso para {recipient_email}! Message ID: {message_id}")
            print(f"E-mail enviado com sucesso para {recipient_email}! Message ID: {message_id}")
        except ClientError as e:
            logging.error(f"Erro ao enviar e-mail para {recipient_email}: {e.response['Error']['Message']}")
            print(f"Erro ao enviar e-mail para {recipient_email}: {e.response['Error']['Message']}")

        time.sleep(1)  # Aguardar 1 segundo entre cada envio, respeitando o limite de SES