# Use official PHP Apache image
FROM php:8.1-apache

# Install OpenVPN and tools
RUN apt-get update && apt-get install -y \
    openvpn \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

# Enable mod_rewrite
RUN a2enmod rewrite

# Set working directory inside container
WORKDIR /var/www/html

# Copy app source code
COPY src /var/www/html

# Give proper permissions to uploads directory
RUN chmod -R 777 /var/www/html/uploads

# Copy VPN config and entrypoint
COPY vpn.ovpn /etc/openvpn/vpn.ovpn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN echo "AKAMSI{file_upload_rce_is_critical}" > /flag.txt

# Expose port 80 (Apache default)
EXPOSE 80

# Start with entrypoint
ENTRYPOINT ["/entrypoint.sh"]
