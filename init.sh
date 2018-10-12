#!/bin/bash

pip install virtualenv
virtualenv -p python3 no_spoilers_env
echo "no_spoilers_env" > .gitignore
source no_spoilers_env/bin/activate
pip3 install -r requirements.txt