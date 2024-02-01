#* Variables
# TODO: use Makefile.venv to activate venv
# include _make/Makefile.venv
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`
PYTHON_VERSION := python3.9

#* Docker variables
IMAGE := eyes3scribe
VERSION := latest
GITHUB := stablecaps
PROJECT_NAME := eyes3scribe

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://install.python-poetry.org | $(PYTHON) - --uninstall

#* Installation
.PHONY: install
install:
	# _make/install_venv.sh $(PYTHON_VERSION) # TODO: get venv activation going
	poetry lock -n && poetry export --without-hashes > requirements.txt
	poetry install -n
	poetry self update
	poetry self add poetry-plugin-up
	poetry up --latest

.PHONY: pre-commit-install
pre-commit-install:
	poetry run pre-commit install

#* Formatters
.PHONY: codestyle
codestyle:
	# poetry run pyupgrade --exit-zero-even-if-changed --py39-plus **/*.py
	poetry run isort --settings-path pyproject.toml ./
	poetry run black --config pyproject.toml ./

.PHONY: formatting
formatting: codestyle

#* Linting
.PHONY: test
test:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=eyes3scribe tests/
	poetry run coverage-badge -o assets/images/coverage.svg -f

.PHONY: check-codestyle
check-codestyle:
	poetry run isort --diff --check-only --settings-path pyproject.toml ./
	poetry run black --diff --check --config pyproject.toml ./
	# poetry run darglint --verbosity 2 eyes3scribe tests

# .PHONY: mypy
# mypy:
# 	poetry run mypy --config-file pyproject.toml ./

# .PHONY: check-safety
# check-safety:
# 	poetry check
# 	poetry run safety check --full-report
# 	# poetry run bandit -ll --recursive eyes3scribe tests

.PHONY: lint
lint: test check-codestyle mypy check-safety

# .PHONY: update-dev-deps
# update-dev-deps:
# 	poetry add -D bandit@latest darglint@latest "isort[colors]@latest" mypy@latest pre-commit@latest pydocstyle@latest pylint@latest pytest@latest pyupgrade@latest safety@latest coverage@latest coverage-badge@latest pytest-html@latest pytest-cov@latest
# 	poetry add -D --allow-prereleases black@latest

#* Docker
# Example: make docker-build VERSION=latest
# Example: make docker-build IMAGE=some_name VERSION=0.1.0
.PHONY: docker-build
docker-build:
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

# Example: make docker-remove VERSION=latest
# Example: make docker-remove IMAGE=some_name VERSION=0.1.0
.PHONY: docker-remove
docker-remove:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)

#* Cleaning
.PHONY: pycache-remove
pycache-remove:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

.PHONY: dsstore-remove
dsstore-remove:
	find . | grep -E ".DS_Store" | xargs rm -rf

# .PHONY: mypycache-remove
# mypycache-remove:
# 	find . | grep -E ".mypy_cache" | xargs rm -rf

.PHONY: ipynbcheckpoints-remove
ipynbcheckpoints-remove:
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf

.PHONY: pytestcache-remove
pytestcache-remove:
	find . | grep -E ".pytest_cache" | xargs rm -rf

.PHONY: build-remove
build-remove:
	rm -rf build/

.PHONY: cleanup
cleanup: pycache-remove dsstore-remove mypycache-remove ipynbcheckpoints-remove pytestcache-remove

.PHONY: ga-initial
ga-initial:
	git add .
	git commit -m ":tada: Initial commit"
	git branch -M master
	git remote add origin git@github.com:$(GITHUB)/$(PROJECT_NAME).git
	git push -u origin master

.PHONY: gen-reposecrets
gen-reposecrets:
	./_make/gen_reposecrets.sh $(PROJECT_NAME) $(DSN)

.PHONY: mod-reposettings
mod-reposettings:
	./_make/mod_reposettings.sh $(PROJECT_NAME)
