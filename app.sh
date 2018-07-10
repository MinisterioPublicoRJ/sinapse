#!/bin/bash
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program waitress-serve --listen=*:8080 sinapse.start:app
