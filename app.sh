#!/bin/bash
source .env 2> /dev/null
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn 'sinapse.start:app' --bind='0.0.0.0:8080'
