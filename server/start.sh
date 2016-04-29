#!/bin/bash
set -e

cd /root/myproject
source /root/myproject/venv/bin/activate

exec /root/myproject/venv/bin/gunicorn -c /root/myproject/server/gun_conf.py gunicorn_server:app