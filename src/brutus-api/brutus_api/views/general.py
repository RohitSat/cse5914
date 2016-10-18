from brutus_api.app import app


@app.route('/')
def index():
    """
    Get the index page.
    """

    return "Brutus API"
