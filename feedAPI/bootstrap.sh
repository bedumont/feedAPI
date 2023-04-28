#!/bin/sh

export FLASK_APP=./feedAPI/index.py
. ./.venv/bin/activate
echo $VIRTUAL_ENV
flask --debug run -h 0.0.0.0
