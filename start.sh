#!/bin/bash
nohup gunicorn --config app.conf.py app:app &
