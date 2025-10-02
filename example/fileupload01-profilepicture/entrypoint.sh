#!/bin/bash
set -e

# Bring up the VPN in the background
openvpn --config /etc/openvpn/vpn.ovpn --daemon

# (Optional) wait for tun0 to come up
echo "Waiting for VPN interface..."
while ! ip link show tun0 >/dev/null 2>&1; do
  sleep 0.5
done
echo "VPN is up, starting Apache."

# Finally, run Apache in the foreground
apache2-foreground