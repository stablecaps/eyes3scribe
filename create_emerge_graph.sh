#!/bin/bash
set -e

mkdir -p emerge_output emerge_input
cp -a launcher.py emerge_input/
cp -a eyes3scribe emerge_input/

emerge -c emerge_config.yaml
