#!/bin/sh

cd $HOME/.local/feedAPI-project/feedAPI
export FLASK_APP=./index.py
. ../.venv/bin/activate
echo $VIRTUAL_ENV
flask --debug run -h 0.0.0.0
