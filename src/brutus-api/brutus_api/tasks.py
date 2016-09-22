from redis import Redis
from rq import get_current_job

from brutus_api import app
from brutus_api import nlp
import json
import requests

from watson_developer_cloud import AuthorizationV1

# TODO move to database
baseurl = "http://127.0.0.1:"
moduleAddresses = {'math': '5010',
                   'weather': '5020',
                   'temperature': '5010',
                   'conditions': '5010'}


def get_answer(text):
    """
    get the answer for a question asked by the user
        -find the module
        -wait for the module to respond
        -set the result
    """

    # get the current job
    redis = Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'])

    job = get_current_job(connection=redis)
    # get the watson username and password
    username = app.config['NLC_WATSON_USERNAME']
    password = app.config['NLC_WATSON_PASSWORD']
    classifierName = app.config['NLC_CLASSIFIER_NAME']
    # set up natural language processor object and pass it the classifier name
    nlc = nlp.Nlp(
        username,
        password,
        classifierName)
    # get the module name
    module = nlc.classify(text)

    url = baseurl + moduleAddresses[module] + "/api/request"
    print(url)
    r = requests.post(url, json={'text': text})
    # get the result from the module
    return r.text.replace("\n", "")
