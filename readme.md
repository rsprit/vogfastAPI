# VOGDB-API

## Setting up

### Starting a MYSQL Server
Write in terminal
```bash
sudo apt-get update
install mysql server
```

set root privileges for the mysql server
```bash
sudo mysql
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
mysql> FLUSH PRIVILEGES;
mysql> exit;
```

If it worked you should be able to access mysql server as root:
```bash
sudo mysql -u root -p
# enter password
```

### Setting up Python environment

python version: 3.8.5

```bash
pip install sqlalchemy
pip install sqlalchemy-utils
pip install pymysql
pip install biopython
pip install hypercorn
pip install fastapi
```
___________________________________________________________________________________________

## Creating the database
* make sure you downloaded the VOGDB data: ftp://ftp.ncbi.nih.gov/pub/COG/COG2020/data
* put the data folder in the same projects folder

1. Create the MYSQL database by running generate_db.py script
> Note: you may need to change the data path or the MYSQL login credentials

Now you should see the newly created tables in the new MYSQL VOG database:
```bash
sudo mysql -u root -p

mysql> show databases;
mysql> use VOGDB;
mysql> show tables;
mysql> describe Protein_profile;

```

## Starting the VOG-API

```bash
cd vogfastAPI
hypercorn vogdb:api --reload
```
