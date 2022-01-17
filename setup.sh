#!/bin/bash

chmod +x ./camera/take_photo.sh

(crontab -l ; echo "0 * * * * /home/pi/projects/window_collage/camera/take_photo.sh")| crontab -
