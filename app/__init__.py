from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)

#load_dotenv()

#app.config['MYSQL_HOST'] = '127.0.0.1' 
#app.config['MYSQL_USER'] = ''
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = ''

#mysql = MySQL(app)

from app import credentials
