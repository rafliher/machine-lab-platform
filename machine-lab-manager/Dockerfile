# Base image
FROM python:3.12-slim

# Env
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/machine-lab-manager

# System deps: add openvpn + easy-rsa
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      gcc libpq-dev \
      openvpn easy-rsa iptables && \
    rm -rf /var/lib/apt/lists/*

# Copy Easy-RSA templates into /etc/openvpn/easy-rsa so we never
# have to call make-cadir at runtime, and symlink `easyrsa` globally.
RUN cp -r /usr/share/easy-rsa /etc/openvpn/easy-rsa && \
    ln -s /usr/share/easy-rsa/easyrsa /usr/local/bin/easyrsa

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code + OpenVPN PKI init scripts
COPY app ./app
COPY scripts ./scripts
COPY .env ./

RUN chmod +x /opt/machine-lab-manager/scripts/*.sh

# Expose & run both services
EXPOSE 8000 1194/udp

# Entrypoint: initialize PKI (if needed) + launch OpenVPN + FastAPI
CMD ["bash","-c","/opt/machine-lab-manager/scripts/init_openvpn.sh && openvpn --config /etc/openvpn/server.conf & uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
