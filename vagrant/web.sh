#!/bin/bash

# install the sqlite3 command line utility
apt-get -y install sqlite3

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
pip install -r /vagrant/src/brutus-module-search/requirements.txt

# install the web app in-place (you can update the code without reinstalling)
pip install -e /vagrant/src/brutus-api
pip install -e /vagrant/src/brutus-module-math
pip install -e /vagrant/src/brutus-module-weather
pip install -e /vagrant/src/brutus-module-search

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
  /vagrant/vagrant/web-upstart-brutus-module-search.conf \
  /etc/init/brutus-module-search.conf

install -o root -g root -m 0644 \
  /vagrant/vagrant/web-upstart-brutus-api-worker.conf \
  /etc/init/brutus-api-worker.conf

initctl reload-configuration
start brutus-api
start brutus-module-math
start brutus-module-weather
start brutus-module-search
start brutus-api-worker

# wait for services to start
sleep 3

# configure the vagrant user's profile
echo 'source /home/vagrant/env/bin/activate' >> /home/vagrant/.profile

# initialize the brutus-api backend database
source "/vagrant/conf/brutus-api.sh"
rm -f "${DATABASE}"

curl -L -s http://127.0.0.1:5000/ > /dev/null
for i in math,http://127.0.0.1:5010 weather,http://127.0.0.1:5020; do
    IFS=',' read name url <<< "${i}"
    curl -s -X POST -H "Content-Type: application/json" \
        -d "{\"name\":\"${name}\",\"url\":\"${url}\"}" \
        http://127.0.0.1:5000/api/module > /dev/null
done
