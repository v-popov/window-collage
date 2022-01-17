#!/bin/bash

yes | sudo apt update && sudo apt upgrade
yes | sudo rpi-update

mkdir projects
cd projects

touch ./env_vars.sh
echo "export CAMERA_DIR=/home/pi/projects/window_collage/camera/" >> env_vars.sh
echo "export DROPBOX_FIRST_HALF_TOKEN='MY_DROPBOX_FIRST_HALF_TOKEN'" >> env_vars.sh
sudo mv ./env_vars.sh /etc/profile.d/

yes | sudo apt install git
echo git --version
git clone -b camera git@github.com:v-popov/window-collage.git

yes | sudo apt install python3-pip
pip install -r ${CAMERA_DIR}requirements.txt

chmod +x ${CAMERA_DIR}take_photo.sh

# (crontab -l ; echo "0 * * * * $CAMERA_DIR/take_photo.sh")| crontab -
# (crontab -l ; echo "10 * * * * /bin/bash -l -exec "/usr/bin/python3 $CAMERA_DIR/dropbox_uploader.py"")| crontab -

(crontab -l ; echo "*/7 * * * * /bin/bash -l -exec '${CAMERA_DIR}take_photo.sh >> /home/pi/projects/window_collage/camera/log_photo.txt 2>&1''")| crontab -
(crontab -l ; echo "*/10 * * * *  /bin/bash -l -exec '/usr/bin/python3 ${CAMERA_DIR}dropbox_uploader.py >> /home/pi/projects/window_collage/camera/log_dropbox.txt 2>&1'")| crontab -

sudo raspi-config

sudo reboot
