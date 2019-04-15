#!/bin/bash
if [ -z "$WORKER" ]
then
    NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn sinapse.url:app --bind=0.0.0.0:8080 --log-file - --access-logfile -
else
    celery -A sinapse.detran.tasks  worker -l info
fi
