from flask import Flask
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from flask_session import Session
import os

app = Flask(__name__)


#Session(app)


app.secret_key = "nuestraClaveSecretaUWU"
load_dotenv('../.env')


app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') 
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

from app import credentials, vehicles, branches, orders
