FROM node:18

# Install OpenVPN and tools
RUN apt-get update && apt-get install -y openvpn iproute2 sudo && rm -rf /var/lib/apt/lists/*

# Create users
RUN useradd -m admin && \
    useradd -m nodeuser

# Set working directory
WORKDIR /app

# Copy source
COPY src /app

# Create the flag file with restricted access
RUN echo "CNCC{stillacutedogthoamiright}" > /flag.txt && \
    chown root:admin /flag.txt && \
    chmod 640 /flag.txt

# Install backend dependencies
WORKDIR /app/backend
RUN npm install

# Install frontend dependencies
WORKDIR /app/frontend
RUN npm install

# Make start script executable
WORKDIR /app
RUN chmod +x start.sh

# Change ownership of app to nodeuser
RUN chown -R nodeuser:nodeuser /app

# Add wait-for-it script
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /wait-for-it.sh
RUN chmod 755 /wait-for-it.sh

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Allow nodeuser to run only base64 as admin with sudo, no password
RUN echo "nodeuser ALL=(admin) NOPASSWD: /usr/bin/base64" > /etc/sudoers.d/nodeuser-admin && \
    chmod 440 /etc/sudoers.d/nodeuser-admin

# Switch to unprivileged user
USER nodeuser

# Expose ports
EXPOSE 80 3000

# Start with entrypoint that handles VPN and then waits for DB
ENTRYPOINT ["/entrypoint.sh"]
