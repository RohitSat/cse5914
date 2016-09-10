# cse5914

## Requirements

* VirtualBox (https://www.virtualbox.org/)
* Vagrant (https://www.vagrantup.com/)

## Quick Start

Start the vagrant VMs.

```
vagrant up
```

Browse some of the available services:

* Brutus API: http://127.0.0.1:5000/
* Brutus Math Module: http://127.0.0.1:5010/

## Local Development

Create a Python 3 virtualenv:

```bash
virtualenv --python=$(which python3) env
source env/bin/activate
```

Install the required python packages:

```bash
pip install -r src/brutus-api/requirements.txt
pip install -r src/brutus-module-math/requirements.txt
```

Install the API and module projects:

```bash
pip install -e $(pwd)/src/brutus-api
pip install -e $(pwd)/src/brutus-module-math
```

Run the API project:

```bash
brutus_api --host 0.0.0.0 --port 5000
```

Run the Math module:

```bash
brutus_module_math --host 0.0.0.0 --port 5010
```

## References

* Python
  * PEP8 Style Guide: https://www.python.org/dev/peps/pep-0008/
  * Pytest: http://docs.pytest.org/en/latest/
