#!/bin/bash

# create a virtualenv for the application
apt-get -y install python-virtualenv python3-dev
virtualenv --python=/usr/bin/python3 /home/vagrant/env

# install python requirements in the virtualenv
source /home/vagrant/env/bin/activate
pip install -r /vagrant/src/brutus-api/requirements.txt
pip install -r /vagrant/src/brutus-math-module/requirements.txt

# install the web app in-place (you can update the code without reinstalling)
pip install -e /vagrant/src/brutus-api
pip install -e /vagrant/src/brutus-math-module

# fix virtualenv permissions (because we're running as root)
chown -R vagrant:vagrant /home/vagrant/env

# setup the hubspy web app and worker
install -o root -g root -m 0644 \
  /vagrant/vagrant/web-upstart-brutus-api.conf \
  /etc/init/brutus-api.conf

install -o root -g root -m 0644 \
  /vagrant/vagrant/web-upstart-brutus-math-module.conf \
  /etc/init/brutus-math-module.conf

initctl reload-configuration
start brutus-api
start brutus-math-module

# configure the vagrant user's profile
echo 'source /home/vagrant/env/bin/activate' >> /home/vagrant/.profile
