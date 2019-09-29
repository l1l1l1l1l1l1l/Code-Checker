#! /bin/bash

export PYTHONPATH=..

python3 -m unittest discover . -p "*_tests.py"
