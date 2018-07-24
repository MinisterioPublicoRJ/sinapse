#!/bin/bash
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn sinapse.url:app --bind=0.0.0.0:8080 --log-file - --access-logfile -