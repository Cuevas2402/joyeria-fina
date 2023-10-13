from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask_session import Session
import os

app = Flask(__name__)


#Session(app)


app.secret_key = "nuestraClaveSecretaUWU"
#load_dotenv()

app.config['MYSQL_HOST'] = '127.0.0.1' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'integracion'

mysql = MySQL(app)

from app import credentials, vehicles, branches
