#!/bin/bash

DATE=$(date +%Y-%m-%d_%H:%M)

raspistill -w 3280 -h 2464 -a 12 -a 1024 -a "%Y-%m-%d %Z%z %p:%X" -ae 64,0x00,0x8080ff,2,0,2300 -n -o ${1}photos/$DATE.jpg
