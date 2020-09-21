#!/bin/bash

refresh_kinit() {
    KINIT_TIMEOUT=$([[ -z "$KINIT_TIMEOUT" ]] && echo 5184000 || echo $KINIT_TIMEOUT);
    echo "Refreshing kinit every $KINIT_TIMEOUT seconds";
    while true; do
        kinit mpmapas@BDA.LOCAL -kt /keys/mpmapas.keytab;
        sleep $KINIT_TIMEOUT;
    done
}

refresh_kinit &
sleep 1;

if [ -z "$WORKER" ]
then
    NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn sinapse.url:app --bind=0.0.0.0:8080 --workers=12 --threads=2 --timeout=60 --log-file - --access-logfile -
else
    celery -A sinapse.tasks worker -l info
fi
