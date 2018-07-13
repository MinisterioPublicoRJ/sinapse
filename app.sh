#!/bin/bash
gunicorn sinapse.start:app --bind=0.0.0.0:8080 --log-file - --access-logfile - 
