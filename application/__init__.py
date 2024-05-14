from flask import Flask
from flask_session import Session

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

app.config['SECRET_KEY'] = "44ec20ec802f8d0a566cacc378c624aaab60f14d06cf7d2137d1e52efd732ca4"

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

uri = "mongodb+srv://kim169:Iwpqo4nbk7LsWaW0@test.qfa1amv.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

from application.routes import about
from application.routes import main
from application.routes import register
