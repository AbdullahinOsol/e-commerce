# e-commerce
(the project is present in master branch of this repository)
(for guidance after office hours, feel free contact me on whatsapp)

install postgresql

run the following commands:
1) CREATE DATABASE ecommerce_database;
2) CREATE USER abdullah WITH PASSWORD 'your_password';
3) GRANT ALL PRIVILEGES ON DATABASE ecommerce_database TO abdullah;

in .env file update the following credentials according to the database and its credentials that you used while creating the db:
# Database Configuration
DB_NAME=ecomdb (replace this whatever database name you set in 1st step of postgresql)
DB_USER=abdullah (replace this whatever user you set in 2nd step of postgresql)
DB_PASSWORD=osolguy1 (replace this whatever password you set in 2nd step of postgresql)
DB_HOST=localhost (check your own host and write that here)
DB_PORT=5433 (change this to 5432)

clone the project and install the libraries in requirements.txt (also add one library 'libmysqlclient-dev', this is not in the txt because this is used while deployment)

after this run the command 'python manage.py runserver'
