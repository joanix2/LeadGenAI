from flask import Flask
from application import routes
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Configurer la connexion à MongoDB
mongo_user = os.getenv('MONGO_ROOT_USERNAME')
mongo_password = os.getenv('MONGO_ROOT_PASSWORD')
mongo_host = os.getenv('MONGO_HOST')
mongo_port = os.getenv('MONGO_PORT')

app.config["MONGO_URI"] = f'mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}'
mongo = PyMongo(app)
