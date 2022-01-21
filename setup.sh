#!/bin/bash

yes | sudo apt update && sudo apt upgrade
yes | sudo rpi-update

mkdir projects

touch ./env_vars.sh
echo "export CAMERA_DIR=/home/pi/projects/window-collage/camera/" >> env_vars.sh
echo "export DROPBOX_FIRST_HALF_TOKEN='MY_DROPBOX_FIRST_HALF_TOKEN'" >> env_vars.sh
sudo mv ./env_vars.sh /etc/profile.d/
source /etc/profile.d/env_vars.sh

yes | sudo apt install git
echo git --version
cd projects
git clone -b camera https://github.com/v-popov/window-collage.git
mkdir window-collage/camera/photos
chmod +x ${CAMERA_DIR}take_photo.sh

yes | sudo apt install python3-pip
pip install -r ${CAMERA_DIR}requirements.txt

EDITOR=nano crontab -e

(crontab -l ; echo "0 * * * * ${CAMERA_DIR}take_photo.sh $CAMERA_DIR > ${CAMERA_DIR}log_photo.txt 2>&1")| crontab -
(crontab -l ; echo "5 * * * * /usr/bin/python3 ${CAMERA_DIR}dropbox_uploader.py --first_half_dropbox_token=$DROPBOX_FIRST_HALF_TOKEN --camera_directory=$CAMERA_DIR > ${CAMERA_DIR}log_dropbox.txt 2>&1")| crontab -

sudo raspi-config

sudo reboot
