# Data Classification Project

This project is designed to classify databases into different levels of criticality. The system processes a JSON file containing information about databases and their classifications, and a CSV file containing information about the responsible managers. When a database is classified as "high," the system sends an email to the responsible manager requesting confirmation of this classification.

## Features

- Processing data from JSON and CSV files stored in encrypted AWS S3.
- Integration with AWS Secrets Manager for managing database access credentials.
- Automatic email sending via AWS SES to database managers with "high" classification.
- Secure connection to RDS PostgreSQL database.
- Detailed logs for tracking data processing and email sending.

## Project Structure

```bash
desafioML/
├── data_processing.py       # Main script for data processing
├── database.py              # Functions related to database connection and operations
├── s3.py                    # Functions for interaction with S3
├── send_email.py            # Functions for sending emails via AWS SES
├── requirements.txt         # Project dependencies
├── Dockerfile               # File for creating the Docker image
├── .env                     # Environment variables file (optional, not included on GitHub)
└── README.md                # Project documentation file
```

# Prerequisites
Before running the project, you will need:

AWS Account: To use S3, SES e Secrets Manager.
PostgreSQL Database: A configured AWS RDS database.
Docker: To run the project in a container.

## 1. AWS Setup
  1. Secrets Manager: Create a secret in AWS Secrets Manager to store PostgreSQL database credentials. The secret name should be rds/credentials/desafioML.

  2. S3 Bucket: Create an S3 bucket and upload the files:

    - classifications.json
    - users.csv
  - SES (Simple Email Service): Verify the email addresses that will be used for sending and receiving emails.

3.Create the database and the owners and database tables in the database
```bash
-- Create database
CREATE DATABASE db_desafioml;

-- Use created database
\c db_desafioml;

-- Create the 'owners' table to store database owners and their managers
CREATE TABLE owners (
    id SERIAL PRIMARY KEY,                 -- Unique identifier for each owner
    owner_email VARCHAR(255) NOT NULL,     -- Email of the database owner
    manager_email VARCHAR(255) NOT NULL    -- Email of the manager responsible for the database
);

-- Create the 'databases' table to store database information and classification
CREATE TABLE databases (
    id SERIAL PRIMARY KEY,                 -- Unique identifier for each database
    database_name VARCHAR(255) NOT NULL,   -- Name of the database
    classification VARCHAR(10) NOT NULL,   -- Classification level of the database (e.g., 'high', 'medium', 'low')
    owner_id INT REFERENCES owners(id)     -- Foreign key linking to the 'owners' table to associate a database with its owner
);
```

## 2. Environment Variables
Create a .env file to configure the required environment variables:

```bash
DPO_EMAIL=dpo_email@domain.com.br
EMAIL_DELIVERY=default_manager@domain.com
```

Alternatively, use the set_env_desafioML.sh script to configure the environment variables:
```bash
#!/bin/bash
# Script para exportar variáveis de ambiente

# Variável de ambiente do DPO (gerente padrão)
export DPO_EMAIL="dpo_email@domain.com.br"

# Variável de ambiente do email de envio pelo SES
export EMAIL_DELIVERY="default_manager@domain.com"

# Exibir as variáveis exportadas para confirmação
echo "DPO_EMAIL=$DPO_EMAIL"
echo "EMAIL_DELIVERY=$EMAIL_DELIVERY"
```
These emails are entered and validated in AWS SES for testing purposes. DPO_EMAIL is used for handling cases where the dataset does not have a located owner and will be used for evaluating and approving the "high" classification. EMAIL_DELIVERY is used as the origin for sending emails via the SES service.

## 3. Docker
To build and run the Docker container:

1. Build the Docker image:
```bash
docker build -t desafio_ml .
```
2. Run the container, passing the .env file with the environment variables:
```bash
docker run --name desafio_ml_container --env-file .env desafio_ml
```

## 4. Database Connection
For security reasons, the parameters and credentials for connecting to the database are stored in AWS Secrets Manager. Ensure that the secret has been configured correctly and the EC2 IAM Role has permission to access this secret.
- Secrets name: rds/credentials/desafioML
- Secret keys: host, database, username, password 

# Execution
The system automatically:

- Downloads JSON and CSV files from S3.
- Processes the information and updates the PostgreSQL database.
- Sends emails to managers responsible for databases classified as "high."

# Useful Command
Remove the container:
```bash
docker rm desafio_ml_container
```
