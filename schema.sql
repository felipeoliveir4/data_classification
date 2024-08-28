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

