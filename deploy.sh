#!/bin/bash
sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y;
sudo apt install awscli postgresql postgresql-contrib python3-pip software-properties-common -y;
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1;
pip install paramiko boto3;    
python main.py; 