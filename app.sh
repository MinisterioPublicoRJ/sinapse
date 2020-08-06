#!/bin/bash
if [ -z "$WORKER" ]
then
    NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn sinapse.url:app --bind=0.0.0.0:8080 --workers=12 --threads=2 --timeout=60 --log-file - --access-logfile -
else
    celery -A sinapse.tasks worker -l info
fi
