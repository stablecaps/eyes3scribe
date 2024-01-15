#!/bin/bash

set -e

mkdir -p images
code2flow --output images/callgraph.png --language py gen_mkdocs_site.py eyes3scribe/*.py eyes3scribe/helpo/*.py

echo -e "\nScript finished"
