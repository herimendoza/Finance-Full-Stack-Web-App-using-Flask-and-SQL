#!/bin/bash

sudo apt update 
sudo apt -y install git
sleep 3
sudo apt -y install python3-pip
sleep 3
git clone https://github.com/bmol5/Finance-Full-Stack-Web-App-using-Flask-and-SQL Finance
sleep 2
cd Finance/
sudo apt-get -y install mysql-server
sudo apt-get -y install libmysqlclient-dev
pip3 install flask-mysqldb
pip install -r requirements.txt
pip install gunicorn
python3 -m gunicorn -w 4 application:app -b 0.0.0.0 --daemon