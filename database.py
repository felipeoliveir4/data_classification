# -*- coding: utf-8 -*-
import psycopg2
import logging
from botocore.exceptions import ClientError
from s3 import get_secret

# Function to connect to the RDS database using Secrets Manager credentials
def connect_rds():
    secret = get_secret()
    if not secret:
        raise Exception("Unable to get Secrets Manager credentials.")

    return psycopg2.connect(
        host=secret['host'],
        database=secret['database'],
        user=secret['username'],
        password=secret['password']
    )

# Function to check if a record already exists in the database
def record_exists(database_name):
    conn = connect_rds()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM databases WHERE database_name = %s', (database_name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

# Function to insert or update data in the PostgreSQL database
def upsert_data_into_db(database_name, classification, owner_email, manager_email):
    conn = connect_rds()
    cursor = conn.cursor()

    if record_exists(database_name):
        # Update existing record
        cursor.execute('''
            UPDATE owners SET owner_email = %s, manager_email = %s
            WHERE id = (SELECT owner_id FROM databases WHERE database_name = %s)
        ''', (owner_email, manager_email, database_name))

        cursor.execute('''
            UPDATE databases SET classification = %s
            WHERE database_name = %s
        ''', (classification, database_name))

        logging.info(f"Updated record: {database_name}")
    else:
        # Insert new record
        cursor.execute('''
            INSERT INTO owners (owner_email, manager_email)
            VALUES (%s, %s)
            RETURNING id
        ''', (owner_email, manager_email))
        owner_id = cursor.fetchone()[0]

        cursor.execute('''
            INSERT INTO databases (database_name, classification, owner_id)
            VALUES (%s, %s, %s)
        ''', (database_name, classification, owner_id))

        logging.info(f"Record inserted: {database_name}")

    conn.commit()
    cursor.close()
