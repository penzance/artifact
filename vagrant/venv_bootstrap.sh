#!/bin/bash
export HOME=/home/vagrant
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv -a /home/vagrant/mapAppDj -r /home/vagrant/mapAppDj/mapAppDj/requirements/local.txt mapAppDj 
