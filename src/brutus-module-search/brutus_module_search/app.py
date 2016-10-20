import os
import uuid
import itertools

from flask import Flask, g, request, render_template, json


# create the flask application
app = Flask(__name__)

app.config.update(
    DEBUG=os.getenv('DEBUG', 'False') in ['true', 'True'],
    SECRET_KEY=os.getenv('SECRET_KEY', str(uuid.uuid4())),
    RAR_WATSON_USERNAME=os.getenv('RAR_WATSON_USERNAME'),
    RAR_WATSON_PASSWORD=os.getenv('RAR_WATSON_PASSWORD'),
    RAR_WATSON_CLUSTER_ID=os.getenv('RAR_WATSON_CLUSTER_ID'),
    RAR_WATSON_COLLECTION_NAME=os.getenv('RAR_WATSON_COLLECTION_NAME'))

