#!/bin/zsh

# settings
VENV="${HOME}/env"
REPO="${HOME}/code/cse5914"

# install ubuntu package tools
sudo apt-get -y install software-properties-common

# install redis
sudo add-apt-repository -y ppa:chris-lea/redis-server
sudo apt-get -y install redis-server

# update environment for python
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"

# create a virtualenv for the application
sudo apt-get -y install python-virtualenv python3-dev
virtualenv --python=/usr/bin/python3 "${VENV}"

# install python requirements in the virtualenv
source "${VENV}/bin/activate"
pip install -r "${REPO}/src/brutus-api/requirements.txt"
pip install -r "${REPO}/src/brutus-module-math/requirements.txt"
pip install -r "${REPO}/src/brutus-module-weather/requirements.txt"
pip install -r "${REPO}/src/brutus-module-jokes/requirements.txt"

# install the web app in-place (you can update the code without reinstalling)
pip install -e "${REPO}/src/brutus-api"
pip install -e "${REPO}/src/brutus-module-math"
pip install -e "${REPO}/src/brutus-module-weather"
pip install -e "${REPO}/src/brutus-module-jokes"

# configure the nitrous user's profile
echo "source ${VENV}/bin/activate" >> "${HOME}/.zprofile"
