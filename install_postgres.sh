#!/bin/bash

# Install PostgreSQL
sudo yum update -y
sudo amazon-linux-extras enable postgresql14
sudo yum install postgresql-server -y
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo su - postgres -c "psql -c \"CREATE DATABASE linkedin_scrapping;\""
sudo su - postgres -c "psql -c \"CREATE USER leoadmin WITH PASSWORD 'fica';\""
sudo su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE linkedin_scrapping TO leoadmin;\""
sudo su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON main_table TO leoadmin;\""
sudo su - postgres -c "psql -c \"ALTER DATABASE linkedin_scrapping SET client_encoding ='UTF8';\""
sudo su - postgres -c "psql -c \"SET CLIENT_ENCODING TO 'utf8';\""
sudo su - postgres -c "psql -c \"ALTER TABLE main_table ADD CONSTRAINT link_unique UNIQUE (link);\""

# Create table
sudo su - postgres -c "psql -d linkedin_scrapping -c \"CREATE TABLE main_table (link text, title text, description text, q varchar, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);\""