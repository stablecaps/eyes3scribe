#!/bin/bash

set -e

mkdir -p images
code2flow --output images/callgraph.png --language py gen_mkdocs_site.py autodocumatix/*.py autodocumatix/helpo/*.py

echo -e "\nScript finished"
