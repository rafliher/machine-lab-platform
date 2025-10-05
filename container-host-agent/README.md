# Container Host Agent

The distributed container management agent for the SiberBox platform. This component runs on host machines to manage Docker containers and communicate with the central Machine Lab Manager.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Registration Process](#registration-process)
- [Deployment Options](#deployment-options)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Overview

The Container Host Agent is a lightweight FastAPI service that:

- **Manages Docker Containers**: Handles container lifecycle operations (create, start, stop, delete)
- **Resource Monitoring**: Reports CPU, memory, and container usage to the manager
- **Secure Communication**: Uses server keys for authenticated communication with the manager
- **Heartbeat System**: Maintains regular connection and health reporting to the central manager
- **Docker Compose Support**: Executes complex multi-container deployments

## Features

### Core Functionality
- ✅ **Container Lifecycle Management**: Create, start, stop, restart, and delete containers
- ✅ **Docker Compose Support**: Handle complex multi-service deployments
- ✅ **Resource Monitoring**: Real-time CPU, memory, and disk usage reporting
- ✅ **Secure Authentication**: Server key-based authentication with the manager
- ✅ **Heartbeat Reporting**: Regular health and status updates to the manager
- ✅ **Network Isolation**: Container network management and isolation

### API Endpoints
- ✅ **Container Operations**: RESTful endpoints for container management
- ✅ **Health Monitoring**: System health and resource usage endpoints
- ✅ **File Management**: Temporary file handling for deployment packages
- ✅ **Docker Integration**: Direct integration with Docker API

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Container Host Agent                        │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Application Server                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │   Docker    │ │  Resource   │ │ Heartbeat   │            │
│  │     API     │ │  Monitor    │ │  Service    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │    File     │ │  Security   │ │   Health    │            │
│  │  Handler    │ │   Module    │ │   Check     │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  Docker Engine Integration                                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │  Container  │ │   Image     │ │   Network   │            │
│  │ Management  │ │ Management  │ │ Management  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │   Volume    │ │  Compose    │                            │
│  │ Management  │ │ Execution   │                            │
│  └─────────────┘ └─────────────┘                            │
├─────────────────────────────────────────────────────────────┤
│  System Resources                                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │     CPU     │ │   Memory    │ │    Disk     │            │
│  │  Monitoring │ │ Monitoring  │ │ Monitoring  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Docker and Docker Compose
- Python 3.8+ (for bare metal deployment)
- Network connectivity to Machine Lab Manager
- Sufficient system resources (CPU, RAM, storage)

### Docker Deployment (Recommended)

1. **Clone and Navigate**
   ```bash
   git clone https://github.com/rafliher/machine-lab-platform.git
   cd machine-lab-platform/container-host-agent
   ```

2. **Register Host in Manager**
   
   First, register this host in the Machine Lab Manager to obtain the required credentials:
   
   ```bash
   # Login to manager to get admin key
   ADMIN_KEY=$(curl -s -X POST "https://your-manager-domain.com/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@yourdomain.com",
       "password": "your_admin_password"
     }' | jq -r '.admin_key')

   # Register this host (save the response)
   curl -X POST "https://your-manager-domain.com/hosts/" \
     -H "Content-Type: application/json" \
     -H "X-Admin-Key: $ADMIN_KEY" \
     -d '{
       "hostname": "host-01",
       "ip": "your-host-ip-address",
       "ssh_port": 22,
       "api_port": 8003,
       "max_containers": 10
     }'
   ```

   Save the returned `id` (Host ID) and `server_key` for configuration.

3. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env
   ```

4. **Deploy Agent**
   ```bash
   docker compose up -d
   ```

5. **Verify Installation**
   ```bash
   curl http://localhost:8003/health
   docker logs container-host-agent -f
   ```

### Bare Metal Deployment

1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip docker.io docker-compose
   pip3 install -r requirements.txt
   ```

2. **Configure Docker Access**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

3. **Configure Environment**
   ```bash
   export JWT_SECRET=your_jwt_secret_key
   export DOCKER_SOCKET=unix:///var/run/docker.sock
   export MANAGER_URL=https://your-manager-domain.com
   export HOST_ID=your_host_id_from_registration
   export SERVER_KEY=your_server_key_from_registration
   export HEARTBEAT_INTERVAL=10
   ```

4. **Start Application**
   ```bash
   python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8003
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```bash
# Authentication (must match manager's JWT_SECRET)
JWT_SECRET=your_jwt_secret_key_minimum_32_characters

# Docker Configuration
DOCKER_SOCKET=unix:///var/run/docker.sock

# Manager Connection
MANAGER_URL=https://your-manager-domain.com
HOST_ID=uuid_provided_during_registration
SERVER_KEY=server_key_provided_during_registration

# Agent Settings
HEARTBEAT_INTERVAL=10  # seconds
API_PORT=8003

# Optional: Resource Limits
MAX_CONTAINERS=10
MAX_CPU_PERCENT=80
MAX_MEMORY_PERCENT=80

# Optional: Logging
LOG_LEVEL=INFO
```

### Docker Compose Configuration

The agent requires access to the Docker socket and network connectivity:

```yaml
version: '3.8'
services:
  container-host-agent:
    build: .
    ports:
      - "8003:8003"
    environment:
      - JWT_SECRET=${JWT_SECRET}
      - DOCKER_SOCKET=${DOCKER_SOCKET}
      - MANAGER_URL=${MANAGER_URL}
      - HOST_ID=${HOST_ID}
      - SERVER_KEY=${SERVER_KEY}
      - HEARTBEAT_INTERVAL=${HEARTBEAT_INTERVAL}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /tmp:/tmp
    network_mode: host  # Required for manager connectivity
    restart: unless-stopped
```

### Quick Start

For a quick setup after obtaining credentials from the manager:

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Configure credentials in .env file
nano .env
# Set: HOST_ID, SERVER_KEY, MANAGER_URL, JWT_SECRET

# 3. Start the agent
docker compose up -d

# 4. Verify connection
curl http://localhost:8003/health
docker logs container-host-agent -f
```

## Registration Process

### Step-by-Step Registration

1. **Access Manager API**
   
   Obtain admin access to the Machine Lab Manager:
   ```bash
   # Login to get admin key
   curl -X POST "https://manager.example.com/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@example.com",
       "password": "admin_password"
     }'
   ```

2. **Register Host**
   
   Register this machine as a container host:
   ```bash
   curl -X POST "https://manager.example.com/hosts/" \
     -H "Content-Type: application/json" \
     -H "X-Admin-Key: your_admin_key" \
     -d '{
       "hostname": "production-host-01",
       "ip": "192.168.1.100",
       "ssh_port": 22,
       "api_port": 8003,
       "max_containers": 20
     }'
   ```

3. **Save Credentials**
   
   From the registration response, save:
   - `id`: Use as `HOST_ID` in agent configuration
   - `server_key`: Use as `SERVER_KEY` in agent configuration

4. **Configure Agent**
   
   Update the agent's `.env` file with the obtained credentials:
   ```bash
   HOST_ID=550e8400-e29b-41d4-a716-446655440000
   SERVER_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

5. **Start Agent**
   
   Deploy the agent and verify connectivity:
   ```bash
   docker compose up -d
   curl http://localhost:8003/health
   ```

### Verification

Verify successful registration by checking the manager:

```bash
# List all hosts to confirm registration
curl -H "X-Admin-Key: your_admin_key" \
  https://manager.example.com/hosts/

# Check specific host status
curl -H "X-Admin-Key: your_admin_key" \
  https://manager.example.com/hosts/your-host-id
```

## Deployment Options

### Development Environment

For development and testing:

```yaml
version: '3.8'
services:
  container-host-agent:
    build: .
    ports:
      - "8003:8003"
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - .:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

### Production Environment

For production deployment with monitoring:

```yaml
version: '3.8'
services:
  container-host-agent:
    image: siberbox/container-host-agent:latest
    ports:
      - "8003:8003"
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /tmp:/tmp
    network_mode: host
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Multi-Host Deployment

Deploy agents across multiple hosts:

```bash
# Host 1
HOST_IP="192.168.1.101"
docker run -d \
  --name container-host-agent \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e HOST_ID=host-1-uuid \
  -e SERVER_KEY=host-1-server-key \
  -e MANAGER_URL=https://manager.example.com \
  siberbox/container-host-agent:latest

# Host 2
HOST_IP="192.168.1.102"
docker run -d \
  --name container-host-agent \
  --network host \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e HOST_ID=host-2-uuid \
  -e SERVER_KEY=host-2-server-key \
  -e MANAGER_URL=https://manager.example.com \
  siberbox/container-host-agent:latest
```

### Kubernetes Deployment

Deploy as a DaemonSet in Kubernetes:

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: container-host-agent
  namespace: siberbox
spec:
  selector:
    matchLabels:
      app: container-host-agent
  template:
    metadata:
      labels:
        app: container-host-agent
    spec:
      hostNetwork: true
      containers:
      - name: agent
        image: siberbox/container-host-agent:latest
        ports:
        - containerPort: 8003
          hostPort: 8003
        env:
        - name: HOST_ID
          valueFrom:
            fieldRef:
              fieldPath: spec.nodeName
        - name: SERVER_KEY
          valueFrom:
            secretKeyRef:
              name: agent-secrets
              key: server-key
        - name: MANAGER_URL
          value: "https://manager.siberbox.com"
        volumeMounts:
        - name: docker-socket
          mountPath: /var/run/docker.sock
        - name: tmp-volume
          mountPath: /tmp
      volumes:
      - name: docker-socket
        hostPath:
          path: /var/run/docker.sock
      - name: tmp-volume
        hostPath:
          path: /tmp
```

## Monitoring

### Health Endpoints

Monitor agent health and status:

```bash
# Basic health check
curl http://localhost:8003/health

# Detailed system information
curl http://localhost:8003/system/info

# Resource usage
curl http://localhost:8003/system/resources
```

### Agent Metrics

Key metrics to monitor:

- **System Resources**: CPU, memory, disk usage
- **Container Count**: Number of active containers
- **Heartbeat Status**: Connection to manager
- **API Response Time**: Agent responsiveness
- **Docker Daemon Status**: Docker engine health

### Logging

Configure structured logging:

```bash
# View agent logs
docker logs container-host-agent -f

# Filter for specific events
docker logs container-host-agent 2>&1 | grep "heartbeat"
docker logs container-host-agent 2>&1 | grep "container"
docker logs container-host-agent 2>&1 | grep "ERROR"
```

### Monitoring Integration

Example Prometheus configuration:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'siberbox-agents'
    static_configs:
      - targets: 
        - 'host1.example.com:8003'
        - 'host2.example.com:8003'
        - 'host3.example.com:8003'
    metrics_path: /metrics
    scrape_interval: 30s
```

## Troubleshooting

### Common Issues

#### 1. Manager Connection Failed

**Symptoms**: Agent cannot connect to manager, heartbeat failures

**Solutions**:
```bash
# Check network connectivity
curl -I https://your-manager-domain.com/health

# Verify credentials
echo $SERVER_KEY | base64 -d  # Should show valid JWT

# Check DNS resolution
nslookup your-manager-domain.com

# Test manager API directly
curl -H "X-Server-Key: $SERVER_KEY" \
  https://your-manager-domain.com/hosts/$HOST_ID/heartbeat \
  -d '{"cpu": 10, "mem": 20, "containers": 0}'
```

#### 2. Docker Socket Permission Denied

**Symptoms**: Cannot access Docker daemon, permission errors

**Solutions**:
```bash
# Check Docker socket permissions
ls -la /var/run/docker.sock

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Test Docker access
docker info
docker ps

# For Docker-in-Docker scenarios
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker:latest docker info
```

#### 3. Container Deployment Failures

**Symptoms**: Containers fail to start, deployment timeouts

**Solutions**:
```bash
# Check Docker daemon status
sudo systemctl status docker
docker info

# Verify available resources
df -h  # Check disk space
free -h  # Check memory
top    # Check CPU usage

# Check Docker logs
sudo journalctl -u docker -f

# Test container creation manually
docker run --rm hello-world
```

#### 4. Host Not Visible in Manager

**Symptoms**: Host appears offline or not registered

**Solutions**:
```bash
# Verify registration
curl -H "X-Admin-Key: admin_key" \
  https://manager.example.com/hosts/ | jq '.[] | select(.ip == "your-host-ip")'

# Check agent logs for connection errors
docker logs container-host-agent --tail 50

# Verify HOST_ID and SERVER_KEY
echo "HOST_ID: $HOST_ID"
echo "SERVER_KEY: ${SERVER_KEY:0:20}..."  # First 20 chars only

# Test heartbeat manually
curl -H "X-Server-Key: $SERVER_KEY" \
  -H "Content-Type: application/json" \
  https://manager.example.com/hosts/$HOST_ID/heartbeat \
  -d '{"cpu": 15, "mem": 30, "containers": 2}'
```

#### 5. High Resource Usage

**Symptoms**: Agent consuming excessive resources

**Solutions**:
```bash
# Monitor agent resource usage
docker stats container-host-agent

# Check for resource leaks
docker system df
docker system prune  # Clean up unused resources

# Monitor system resources
htop
iotop
```

### Debug Mode

Enable debug logging for troubleshooting:

```bash
# Set debug environment
docker compose down
echo "LOG_LEVEL=DEBUG" >> .env
docker compose up -d

# Or restart with debug
docker run -it --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -e LOG_LEVEL=DEBUG \
  -e HOST_ID=$HOST_ID \
  -e SERVER_KEY=$SERVER_KEY \
  -e MANAGER_URL=$MANAGER_URL \
  siberbox/container-host-agent:latest
```

### Performance Tuning

#### Resource Optimization

```bash
# Limit agent resource usage
docker run -d \
  --memory=512m \
  --cpus=1.0 \
  --name container-host-agent \
  siberbox/container-host-agent:latest

# Configure Docker daemon limits
sudo nano /etc/docker/daemon.json
{
  "default-runtime": "runc",
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

#### Network Optimization

```bash
# Use host networking for better performance
docker run -d \
  --network host \
  --name container-host-agent \
  siberbox/container-host-agent:latest

# Configure heartbeat interval
HEARTBEAT_INTERVAL=30  # Reduce frequency for lower network usage
```

### Security Hardening

#### Network Security

```bash
# Restrict agent API access
iptables -A INPUT -p tcp --dport 8003 -s manager-ip -j ACCEPT
iptables -A INPUT -p tcp --dport 8003 -j DROP

# Use TLS for manager communication
export MANAGER_URL=https://manager.example.com  # Always use HTTPS
```

#### Container Security

```bash
# Run agent with limited privileges
docker run -d \
  --user 1000:1000 \
  --read-only \
  --tmpfs /tmp \
  siberbox/container-host-agent:latest

# Scan images before deployment
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image siberbox/container-host-agent:latest
```

### Support Resources

- **Manager API Documentation**: Available at manager's `/api-docs` endpoint
- **GitHub Issues**: [Report bugs and feature requests](https://github.com/rafliher/machine-lab-platform/issues)
- **Main Documentation**: See project root README for overall platform documentation
- **Docker Documentation**: [Docker engine reference](https://docs.docker.com/engine/)

For additional support, please refer to the main project documentation or create an issue in the GitHub repository.

> **Note**: Ensure the host machine has sufficient resources (CPU, RAM, storage) to run both the agent and the containers it will manage. The agent itself is lightweight but containers may require significant resources depending on the deployed applications.