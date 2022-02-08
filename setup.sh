#!/bin/bash

yes | sudo apt update && sudo apt upgrade

sudo apt-get install gifsicle

yes | sudo apt-get install libatlas-base-dev

mkdir projects

touch ./env_vars.sh
echo "export SERVER_DIR=/home/pi/projects/window-collage/server/" >> env_vars.sh
echo "export DROPBOX_FIRST_HALF_TOKEN='MY_DROPBOX_FIRST_HALF_TOKEN'" >> env_vars.sh
sudo mv ./env_vars.sh /etc/profile.d/
source /etc/profile.d/env_vars.sh

yes | sudo apt install git
echo git --version
cd projects
git clone -b server https://github.com/v-popov/window-collage.git

mkdir ${SERVER_DIR}photos

yes | sudo apt install python3-pip
pip install -r ${SERVER_DIR}requirements.txt

EDITOR=nano crontab -e

(crontab -l ; echo "10 * * * * /usr/bin/python3 ${SERVER_DIR}dropbox_reorganizer.py --first_half_dropbox_token=$DROPBOX_FIRST_HALF_TOKEN > ${SERVER_DIR}log_dropbox.txt 2>&1")| crontab -

sudo reboot
