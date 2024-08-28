# -*- coding: utf-8 -*-
import boto3
from botocore.exceptions import ClientError
import logging
import time

# Logging configuration
logging.basicConfig(
    filename='email_test.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Function to send emails one at a time
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
            logging.info(f"Email sent successfully to {recipient_email}! Message ID: {message_id}")
            print(f"Email sent successfully to {recipient_email}! Message ID: {message_id}")
        except ClientError as e:
            logging.error(f"Email sent successfully to {recipient_email}: {e.response['Error']['Message']}")
            print(f"Email sent successfully to {recipient_email}: {e.response['Error']['Message']}")

        time.sleep(1)  # Wait 1 second between each sending, respecting the SES limit