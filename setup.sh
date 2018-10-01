#!usr/#!/usr/bin/env bash
sudo apt-get install python3-pip
pip3 install termcolor
git clone https://github.com/Shiranuit/project_setup.git ~/project_setup
sudo cp ~/project_setup/project.py /usr/bin/project
