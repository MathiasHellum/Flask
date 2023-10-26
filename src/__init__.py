from flask import Flask

app = Flask(__name__)
app.json.sort_keys = False


# Importing the controllers for the app
from src.controllers import *
