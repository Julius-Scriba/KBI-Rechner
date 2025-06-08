#!/bin/bash
# Enable SSL for Maerkischer Hofladen using certbot and nginx

set -e

DOMAIN_IDN="xn--mrkischerhofladen-qqb.de"
EMAIL="admin@maerkischerhofladen.de"
NGINX_CONF="/etc/nginx/sites-available/maerkischerhofladen.conf"
SSL_SNIPPET="/etc/nginx/snippets/ssl-params.conf"

# install certbot if not available
if ! command -v certbot >/dev/null 2>&1; then
    if command -v snap >/dev/null 2>&1; then
        sudo snap install core
        sudo snap refresh core
        sudo snap install --classic certbot
        sudo ln -sf /snap/bin/certbot /usr/bin/certbot
    else
        sudo apt update
        sudo apt install -y certbot python3-certbot-nginx
    fi
fi

# backup nginx config
if [ -f "$NGINX_CONF" ]; then
    sudo cp "$NGINX_CONF" "${NGINX_CONF}.bak.$(date +%F-%H%M)"
fi

# create recommended ssl params
if [ ! -f "$SSL_SNIPPET" ]; then
    sudo tee "$SSL_SNIPPET" > /dev/null <<'PARAMS'
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256';
ssl_prefer_server_ciphers off;
ssl_ecdh_curve X25519:secp384r1;
ssl_dhparam /etc/ssl/certs/dhparam.pem;
PARAMS
fi

if [ ! -f /etc/ssl/certs/dhparam.pem ]; then
    sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
fi

# obtain certificate and configure nginx
sudo certbot --nginx \
    -d "$DOMAIN_IDN" \
    -d "www.$DOMAIN_IDN" \
    --non-interactive --agree-tos -m "$EMAIL" --redirect

# ensure ssl params snippet included
if ! grep -q "ssl-params.conf" "$NGINX_CONF"; then
    sudo sed -i '/ssl_certificate_key/a \    include snippets/ssl-params.conf;' "$NGINX_CONF"
fi

sudo nginx -t
sudo systemctl reload nginx

