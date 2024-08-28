# -*- coding: utf-8 -*-
import os
import json
import pandas as pd
import logging
import time
from io import StringIO
from database import upsert_data_into_db
from s3 import download_file_from_s3
from send_email import send_emails

# Configure logging
logging.basicConfig(
    filename='data_processing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Name of the S3 bucket and the files inside it
bucket_name = 'bucket-desafioml'
json_file_s3 = 'classifications.json'
csv_file_s3 = 'users.csv'

# Use environment variables to avoid hardcoded emails
dpo = os.getenv("DPO_EMAIL", "default_dpo@domain.com")
email_delivery = os.getenv("EMAIL_DELIVERY", "default_email_sender@domain.com")

# Function to process CSV file
def process_csv(csv_content):
    csv_data = pd.read_csv(StringIO(csv_content))
    owner_manager_map = {}

    for index, row in csv_data.iterrows():
        user_id = row['user_id']
        manager_email = row['user_manager']
        owner_manager_map[user_id] = manager_email

    return owner_manager_map

# Function to send email if rating is "high"
def check_and_send_email(database_name, classification, manager_email):
    if classification == 'high':
        logging.info(f"Database {database_name} classified as 'high'. Sending email to manager {manager_email}...")

        subject = f"Approval Needed for {database_name} Database Classification"
        body_text = (f"Dear Manager,\n\n"
                     f"As part of our annual database classification review, the database '{database_name}' has been marked as 'high' criticality. "
                     f"Please confirm the 'high' classification for '{database_name}' or let us know if any adjustments are needed.\n\n"
                     "Best regards,\n"
                     "Meli Security Team")

        # Call the email sending script
        send_emails(email_delivery, [manager_email], subject, body_text)

        # Wait 1 second between submissions to avoid violating SES limits
        time.sleep(1)

# Download and process JSON file from S3
json_content = download_file_from_s3(bucket_name, json_file_s3)
json_data = json.loads(json_content)

# Download and process CSV file from S3
csv_content = download_file_from_s3(bucket_name, csv_file_s3)
owner_manager_map = process_csv(csv_content)

# Process each record in the JSON file
for record in json_data:
    if 'database_name' not in record:
        logging.warning(f"Skipping record due to missing database name: {record}")
        continue

    if 'owner_email' not in record:
        record['owner_email'] = 'unknown_email@meli.com'

    owner_id = record.get('owner_id')
    
    if owner_id in owner_manager_map:
        manager_email = owner_manager_map[owner_id]
    else:
        manager_email = dpo

    # Insert or update data in the database
    upsert_data_into_db(
        database_name=record['database_name'],
        classification=record['classification'],
        owner_email=record['owner_email'],
        manager_email=manager_email
    )

    # Check and send the email after inserting it into the database
    check_and_send_email(
        database_name=record['database_name'],
        classification=record['classification'],
        manager_email=manager_email
    )

logging.info("Data processing completed.")
print("Data processing completed.")