#!/usr/bin/env bash
git clone https://github.com/Shiranuit/project_setup_epitech.git ~/project_setup
sudo rm /usr/bin/project
sudo cp ~/project_setup/project.py /usr/bin/project
sudo rm ~/project_setup -r -f
