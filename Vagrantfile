# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
    # common
    config.vm.box = "ubuntu/trusty64"
    config.vm.provision "shell", path: "vagrant/common.sh"

    # web vm
    config.vm.define "web" do |web|
        web.vm.hostname = "web"
        web.vm.provider "virtualbox" do |vb|
            vb.memory = 512
            vb.cpus = 1
        end

        web.vm.provision "shell", path: "vagrant/web.sh"
        web.vm.network "forwarded_port", guest: 5000, host: 5000
        web.vm.network "forwarded_port", guest: 5010, host: 5010
        web.vm.network "forwarded_port", guest: 5020, host: 5020
    end
end
