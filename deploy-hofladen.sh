#!/bin/bash
# Deployment script for Maerkischer Hofladen Flask application

set -e

APP_DIR="$(dirname "$0")"
VENV="$APP_DIR/venv"

if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt"
pip install gunicorn

echo "Creating systemd service file..."
SERVICE_FILE="/etc/systemd/system/maerkischerhofladen.service"
cat <<SERVICE > maerkischerhofladen.service
[Unit]
Description=Maerkischer Hofladen Flask App
After=network.target

[Service]
User=hofladen
WorkingDirectory=$APP_DIR
Environment=FLASK_APP=app
Environment=FLASK_ENV=production
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:5001 app:app
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

sudo mv maerkischerhofladen.service "$SERVICE_FILE"

sudo systemctl daemon-reload
sudo systemctl enable maerkischerhofladen.service
sudo systemctl restart maerkischerhofladen.service

echo "Deployment completed."
