#!/bin/bash

# curl https://raw.githubusercontent.com/v-popov/window-collage/camera/setup.sh -o setup.sh
# yes | sudo bash setup.sh

yes | sudo apt update && sudo apt upgrade
yes | sudo rpi-update

sudo mkdir projects

touch ./env_vars.sh
echo "export CAMERA_DIR=/home/pi/projects/window-collage/camera/" >> env_vars.sh
echo "export DROPBOX_FIRST_HALF_TOKEN='MY_DROPBOX_FIRST_HALF_TOKEN'" >> env_vars.sh
sudo mv ./env_vars.sh /etc/profile.d/

yes | sudo apt install git
echo git --version
cd projects
sudo git clone -b camera https://github.com/v-popov/window-collage.git
mkdir photos

sudo mv ${CAMERA_DIR}CameraCron /etc/cron.d/CameraCron
sudo mv ${CAMERA_DIR}DropboxCron /etc/cron.d/DropboxCron

yes | sudo apt install python3-pip
pip install -r ${CAMERA_DIR}requirements.txt

chmod +x ${CAMERA_DIR}take_photo.sh

# (crontab -l ; echo "0 * * * * $CAMERA_DIR/take_photo.sh")| crontab -
# (crontab -l ; echo "10 * * * * /bin/bash -l -exec "/usr/bin/python3 $CAMERA_DIR/dropbox_uploader.py"")| crontab -

# (crontab -l ; echo "*/7 * * * * /bin/bash -l -exec '${CAMERA_DIR}take_photo.sh >> /home/pi/projects/window_collage/camera/log_photo.txt 2>&1''")| crontab -
# (crontab -l ; echo "*/10 * * * *  /bin/bash -l -exec '/usr/bin/python3 ${CAMERA_DIR}dropbox_uploader.py >> /home/pi/projects/window_collage/camera/log_dropbox.txt 2>&1'")| crontab -

#echo "*/7 * * * * /bin/bash -l -exec '${CAMERA_DIR}take_photo.sh >> ${CAMERA_DIR}log_photo.txt 2>&1'" >/etc/cron.d/take_photo
#echo "*/10 * * * *  /bin/bash -l -exec '/usr/bin/python3 ${CAMERA_DIR}dropbox_uploader.py >> ${CAMERA_DIR}log_dropbox.txt 2>&1'" >/etc/cron.d/dropbox_uploader

sudo raspi-config

sudo reboot
