#!/bin/zsh

# settings
VENV="${HOME}/env"
REPO="${HOME}/code/cse5914"
PIP_OPTS="--ignore-installed --no-cache-dir"

# install ubuntu package tools
sudo apt-get -y install software-properties-common

# install redis
sudo add-apt-repository -y ppa:chris-lea/redis-server
sudo apt-get -y install redis-server

# create a virtualenv for the application
sudo apt-get -y install python-virtualenv python3-dev
virtualenv --python=/usr/bin/python3 "${VENV}"
pip ${PIP_OPTS} install --upgrade pip setuptools

# install python requirements in the virtualenv
source "${VENV}/bin/activate"
pip ${PIP_OPTS} install -r "${REPO}/src/brutus-api/requirements.txt"
pip ${PIP_OPTS} install -r "${REPO}/src/brutus-module-math/requirements.txt"
pip ${PIP_OPTS} install -r "${REPO}/src/brutus-module-weather/requirements.txt"

# install the web app in-place (you can update the code without reinstalling)
pip ${PIP_OPTS} install -e "${REPO}/src/brutus-api"
pip ${PIP_OPTS} install -e "${REPO}/src/brutus-module-math"
pip ${PIP_OPTS} install -e "${REPO}/src/brutus-module-weather"

# configure the vagrant user's profile
echo "source ${VENV}/bin/activate" >> "${HOME}/.zprofile"
