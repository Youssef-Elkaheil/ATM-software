#!/bin/bash

source ~/Desktop/setEmail.sh

cd ~/Desktop/ATM-software/

# uncomment when using raspberry pi
#export RASPBERRY_PI=1

python3 ./main.py
