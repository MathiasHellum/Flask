from flask import Flask

app = Flask(__name__)

# Importing the controllers for the app
from src.controllers import *
