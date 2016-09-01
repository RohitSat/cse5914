#!/bin/bash

# update packages
apt-get update
apt-get -y upgrade

# install development tools and utilities
apt-get -y install vim git tmux htop unzip

# create a section in the vagrant user's .bashrc for local aliases
echo '' >> /home/vagrant/.bashrc
echo '# local aliases' >> /home/vagrant/.bashrc

# create a section in the vagrant user's .profile for local variables
echo '' >> /home/vagrant/.profile
echo '# local settings' >> /home/vagrant/.profile
