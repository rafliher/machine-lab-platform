FROM python:3.11-slim

WORKDIR /app

# Install dependencies for VPN
RUN apt-get update && apt-get install -y \
    openvpn iproute2 \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .
COPY vpn.ovpn /etc/vpn.ovpn

# Make entrypoint executable
RUN chmod +x entrypoint.sh

EXPOSE 80 8080

CMD ["./entrypoint.sh"]