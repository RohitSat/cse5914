from redis import Redis
from rq import get_current_job

from brutus_api import app
from brutus_api import nlp
import requests
import json

from watson_developer_cloud import AuthorizationV1


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

    # set up natural language processor object and pass it the classifier name
    nlc = nlp.Nlp(
        app.config['NLC_WATSON_USERNAME'],
        app.config['NLC_WATSON_PASSWORD'],
        app.config['NLC_CLASSIFIER_NAME'])

    # get the module name
    module = nlc.classify(text)

    # get the result from the module
    url = baseurl + moduleAddresses[module] + "/api/request"
    r = requests.post(url, json={'input': {'text': text}})

    if r.text is None:
        return {'text': 'I am sorry, an error occurred'}

    jsonResult = json.loads(r.text)
    return jsonResult['output']
