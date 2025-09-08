#!/bin/bash
set -e

# Check if VPN config exists and start VPN if it does
if [ -f /etc/openvpn/vpn.ovpn ]; then
    echo "VPN config found, starting OpenVPN..."
    openvpn --config /etc/openvpn/vpn.ovpn --daemon
    
    # Wait for tun0 to come up
    echo "Waiting for VPN interface..."
    while ! ip link show tun0 >/dev/null 2>&1; do
        sleep 0.5
    done
    echo "VPN is up!"
else
    echo "No VPN config found, skipping VPN setup..."
fi

# Wait for database and start the application
exec /wait-for-it.sh db:3306 -- ./start.sh
