#!/bin/bash

sudo apt update
sudo apt -y upgrade
sudo apt -y install git
sleep 3
sudo apt -y install python3-pip
pip install --upgrade pip
sleep 3
git clone https://github.com/bmol5/Finance-Full-Stack-Web-App-using-Flask-and-SQL Finance
sleep 2
cd Finance/
sudo apt-get -y install mysql-server
sudo apt-get -y install libmysqlclient-dev
pip3 install flask-mysqldb
pip install -r requirements.txt
sed '50!d' < application.py
cat outputs.txt > .env
sql_uri=$(cat outputs.txt | sed '2!d')
echo $sql_uri
export DB_URI=$(echo $sql_uri)
source .env
export FLASK_APP=application
flask run --host=0.0.0.0
