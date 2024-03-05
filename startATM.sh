#!/bin/bash

source ./setEmail.sh

# set project absolute location
cd ~/Desktop/ATM-software/

# uncomment when using raspberry pi
#export RASPBERRY_PI=1

python3 ./main.py
