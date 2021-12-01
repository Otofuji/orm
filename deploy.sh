#!/bin/bash
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y; 
sudo apt install postgresql postgresql-contrib python3-pip -y;
pip3 install flask requests;
git clone https://github.com/raulikeda/tasks.git;
cd tasks;
./install.sh;
sudo ufw allow 8080/tcp;
sudo reboot;