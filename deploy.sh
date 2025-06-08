#!/bin/bash
# Deployment script for KBI-Rechner Flask application

set -e

APP_DIR="$(dirname "$0")"
VENV="$APP_DIR/venv"

if [ ! -d "$VENV" ]; then
    python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt"

echo "Creating systemd service file..."
SERVICE_FILE="/etc/systemd/system/kbi-rechner.service"
cat <<SERVICE > kbi-rechner.service
[Unit]
Description=KBI Rechner Flask App
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$APP_DIR
Environment=FLASK_APP=app
Environment=FLASK_ENV=production
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
SERVICE

sudo mv kbi-rechner.service "$SERVICE_FILE"

echo "Reloading systemd daemon and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable kbi-rechner.service
sudo systemctl restart kbi-rechner.service

echo "Deployment completed."

