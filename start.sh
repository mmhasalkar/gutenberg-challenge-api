#!/bin/bash
gunicorn -w 3 --timeout 300 --pid process.pid --bind 0.0.0.0:7000 --daemon run:app --access-logfile logs/access.log --error-logfile logs/error.log
echo "Service Started!"
