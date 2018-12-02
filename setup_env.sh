#!/usr/bin/env bash
pip install virtualenv --user
virtualenv venv -p python3
source ./venv/bin/activate
pip install -r reqs.txt
