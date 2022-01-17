# curl https://raw.githubusercontent.com/v-popov/window-collage/camera/setup2.sh -o setup2.sh
# yes | sudo bash setup2.sh

echo "*/7 * * * * /bin/bash -l -exec '${CAMERA_DIR}take_photo.sh'" >/etc/cron.d/take_photo
echo "*/10 * * * *  /bin/bash -l -exec '/usr/bin/python3 ${CAMERA_DIR}dropbox_uploader.py'"
pip install -r ${CAMERA_DIR}requirements.txt
chmod +x ${CAMERA_DIR}take_photo.sh
