#!/bin/bash

# install redis
add-apt-repository -y ppa:chris-lea/redis-server
apt-get update
apt-get -y install redis-server

# configure redis to bind to all interfaces (so we can reach it outside the VM)
sed -i -e 's/bind 127.0.0.1/bind 0.0.0.0/g' /etc/redis/redis.conf

# create a virtualenv for the application
apt-get -y install python-virtualenv python3-dev
virtualenv --python=/usr/bin/python3 /home/vagrant/env

# install python requirements in the virtualenv
source /home/vagrant/env/bin/activate
pip install -r /vagrant/src/brutus-api/requirements.txt
pip install -r /vagrant/src/brutus-module-math/requirements.txt
pip install -r /vagrant/src/brutus-module-weather/requirements.txt

# install the web app in-place (you can update the code without reinstalling)
pip install -e /vagrant/src/brutus-api
pip install -e /vagrant/src/brutus-module-math
pip install -e /vagrant/src/brutus-module-weather

# fix virtualenv permissions (because we're running as root)
chown -R vagrant:vagrant /home/vagrant/env

# setup the brutus-api web app and worker
install -o root -g root -m 0644 \
  /vagrant/vagrant/web-upstart-brutus-api.conf \
  /etc/init/brutus-api.conf

install -o root -g root -m 0644 \
  /vagrant/vagrant/web-upstart-brutus-module-math.conf \
  /etc/init/brutus-module-math.conf

  install -o root -g root -m 0644 \
    /vagrant/vagrant/web-upstart-brutus-module-weather.conf \
    /etc/init/brutus-module-weather.conf

install -o root -g root -m 0644 \
  /vagrant/vagrant/web-upstart-brutus-api-worker.conf \
  /etc/init/brutus-api-worker.conf

initctl reload-configuration
start brutus-api
start brutus-module-math
start brutus-module-weather
start brutus-api-worker

# configure the vagrant user's profile
echo 'source /home/vagrant/env/bin/activate' >> /home/vagrant/.profile
