# cse5914

[![Build Status](https://travis-ci.org/RohitSat/cse5914.svg?branch=master)](https://travis-ci.org/RohitSat/cse5914)

## Requirements

* VirtualBox (https://www.virtualbox.org/)
* Vagrant (https://www.vagrantup.com/)

## Quick Start

[![Nitrous Quickstart](https://nitrous-image-icons.s3.amazonaws.com/quickstart.svg)](https://www.nitrous.io/quickstart)

Start the vagrant VMs.

```
vagrant up
```

Browse some of the available services:

* Brutus API: http://127.0.0.1:5000/
* Brutus Math Module: http://127.0.0.1:5010/
* Brutus Weather Module: http://127.0.0.1:5020/

## Local Development

Create a Python 3 virtualenv:

```bash
virtualenv --python=$(which python3) env
source env/bin/activate
```

Install the required python packages:

```bash
pip install -r src/brutus-api/requirements.txt
```

Install the project as an in-place editable package:

```bash
pip install -e $(pwd)/src/brutus-api
```

Run the project:

```bash
brutus_api --host 0.0.0.0 --port 5000
```

Run the worker for background tasks:

```bash
rq worker
```

## Tests

Navigate to the project directory and run the tests using Make targets:

```bash
cd src/brutus-api
make test-style  # run style tests
make test-unit   # run unit tests
make test        # run all tests
```

## References

* Python
  * PEP8 Style Guide: https://www.python.org/dev/peps/pep-0008/
  * Python RQ: http://python-rq.org/docs/
  * Pytest: http://docs.pytest.org/en/latest/
  * Responses: https://github.com/getsentry/responses
  * HTTTPretty: https://github.com/gabrielfalcao/HTTPretty
