#!/bin/bash

# this script is used to upload the final_project directory to the Brickpi Desktop/TEAM11 directory
# without going through a gui like FileZilla

sshpass -p "robots1234" scp -r ../final_project/ pi@192.168.50.5:Desktop/TEAM11
