import os
import uuid
import itertools

from flask import Flask, g, request, render_template, json


# create the flask application
app = Flask(__name__)

app.config.update(
    DEBUG=os.getenv('DEBUG', 'False') in ['true', 'True'],
    SECRET_KEY=os.getenv('SECRET_KEY', str(uuid.uuid4())))
