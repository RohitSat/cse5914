#!/usr/bin/env python

import argparse

from werkzeug.serving import run_simple

from brutus_api import app


def main():
    """
    Run the web application from the console.
    """

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1", help="listen host")
    parser.add_argument("--port", type=int, default=5010, help="listen port")

    args = parser.parse_args()

    # run the application
    run_simple(args.host, args.port, app, use_reloader=True, use_debugger=True)
