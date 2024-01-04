#!/bin/bash

set -e


pydeps --noshow --exclude rich sentry_sdk yaml sys dotmap bashautodoc.regex_patterns --rankdir RL --reverse -- launcher.py

mv launcher.svg images/launcher.svg
