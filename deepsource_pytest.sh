#!/bin/bash

set -eu

# Install pytest and pytest-cov pacakages from pip
pip install pytest pytest-cov

# Run pytest with --cov and --cov-report flags
pytest --cov=./ --cov-report xml

# Install deepsource CLI
curl https://deepsource.io/cli | sh

# Set DEEPSOURCE_DSN env variable from repository settings page
# must be exported befoire
export DEEPSOURCE_DSN=${PRIVATE_REPO_DSN}

# From the root directory, run the report coverage command
./bin/deepsource report --analyzer test-coverage --key python --value-file ./coverage.xml
