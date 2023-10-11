from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)

#load_dotenv()

#app.config['MYSQL_HOST'] = '127.0.0.1' 
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'camaro.Z28'
#app.config['MYSQL_DB'] = 'soiree'

#mysql = MySQL(app)

from app import credentials
