#!/usr/bin/env bash
set -e

EASYRSA_DIR=/etc/openvpn/easy-rsa
PKI_DIR="$EASYRSA_DIR/pki"

# Only initialize if the CA cert isn't already there
if [ ! -f "$PKI_DIR/ca.crt" ]; then
  echo "Initializing OpenVPN PKI…"

  # If an empty PKI_DIR was created by Docker, remove it so easyrsa can init
  if [ -d "$PKI_DIR" ] && [ ! -s "$PKI_DIR" ]; then
    rm -rf "$PKI_DIR"
  fi

  cd "$EASYRSA_DIR"

  # Non-interactive mode: either export EASYRSA_BATCH=1 or pass --batch
  # Here we use the --batch flag on each call.
  ./easyrsa --batch init-pki
  ./easyrsa --batch build-ca nopass
  ./easyrsa gen-dh
  openvpn --genkey --secret ta.key

  # Build server cert, non-interactive
  ./easyrsa --batch build-server-full server nopass

  # Write the server.conf
  cat > /etc/openvpn/server.conf <<'EOF'
port 1194
proto udp
dev tun
ca /etc/openvpn/easy-rsa/pki/ca.crt
cert /etc/openvpn/easy-rsa/pki/issued/server.crt
key /etc/openvpn/easy-rsa/pki/private/server.key
dh /etc/openvpn/easy-rsa/pki/dh.pem
tls-auth /etc/openvpn/easy-rsa/ta.key 0
keepalive 10 120
persist-key
persist-tun
user nobody
group nogroup
verb 3
server 10.8.0.0 255.255.255.0
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
EOF

  echo "OpenVPN PKI initialized."
else
  echo "OpenVPN PKI already exists, skipping init."
fi
