import itertools

from flask import g, request, render_template, json

from brutus_api import app
from brutus_api.tasks import get_answer


def get_job_details(job):
    return {
        'id': job.id,
        'status': job.get_status(),
        'input': {'text': job.meta['input']},
        'output': job.result}


@app.route('/')
def index():
    """
    Get the index page.
    """

    return "Brutus API"


@app.route('/api/request', methods=['GET', 'POST'])
def create_request():
    """
    Get requests or create a new request.
    """

    if request.method == 'GET':
        # retrieve started, queued, and finished jobs
        job_ids = itertools.chain(
            g.started_registry.get_job_ids(),
            g.finished_registry.get_job_ids())

        jobs = itertools.chain(
            g.queue.get_jobs(),
            [g.queue.fetch_job(job_id) for job_id in job_ids])

        # return requests and their status
        return json.jsonify([get_job_details(job) for job in jobs])

    # create the job
    data = request.get_json()
    job = g.queue.enqueue(get_answer, data['text'])
    job.meta['input'] = data['text']
    job.save()

    # return the request information
    return json.jsonify(get_job_details(job))


@app.route('/api/request/<uuid:request_id>')
def get_request(request_id):
    """
    Get a request.
    """

    job = g.queue.fetch_job(str(request_id))
    return json.jsonify(get_job_details(job))
