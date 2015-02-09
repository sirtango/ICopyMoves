#!/bin/sh

PYTHONPATH=$(dirname "$(readlink -f "$0")")
PYTHON=$(which python)

PYTHONPATH=$PYTHONPATH $PYTHON -u -m copybot

