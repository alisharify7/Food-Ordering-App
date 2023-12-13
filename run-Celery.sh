#!/usr/bin/bash

celery -A make_celery worker -l info -E