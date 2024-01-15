#!/bin/bash

set -e

rm -rfv emerge_output emerge_input
mkdir -p emerge_output emerge_input
cp -a launcher.py emerge_input/
cp -a eyes3scribe emerge_input/


find ./emerge_input -name "*.pyc" -exec rm -fv {} \; || true
find ./emerge_input -name "__pycache__" -exec rm -rfv {} \; || true

emerge -c emerge_config.yaml
