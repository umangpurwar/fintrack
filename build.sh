#!/usr/bin/env bash
# build.sh — Render build script
# Runs on every deployment before the app starts.
# SRS: NFR-REL-01 — Render free tier deployment

set -o errexit
# Exit immediately if any command fails. Prevents partial deployments.

pip install -r requirements.txt
# Install all pinned dependencies.

python manage.py collectstatic --noinput
# Gather static files into staticfiles/ for WhiteNoise to serve.

python manage.py migrate
# Run any new database migrations.
# This runs every deployment — Django is smart enough to skip already-applied migrations.
