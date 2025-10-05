# Machine Lab Manager

The central API server and VPN manager for the SiberBox platform. This component handles container orchestration, host management, user authentication, and VPN provisioning.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [VPN Integration](#vpn-integration)
- [Deployment Options](#deployment-options)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

## Overview

The Machine Lab Manager is the core component of the SiberBox platform, providing:

- **RESTful API**: Comprehensive API for all platform operations
- **Container Orchestration**: Manages deployment across multiple hosts
- **VPN Server**: Integrated OpenVPN server with automatic client provisioning
- **Database Management**: PostgreSQL-based data persistence
- **Authentication**: JWT-based admin authentication and API key management
- **Load Balancing**: Intelligent container distribution based on host capacity

## Features

### Core Functionality
- ✅ **Multi-Host Container Management**: Deploy and manage containers across distributed hosts
- ✅ **Automatic VPN Provisioning**: Generate unique OpenVPN profiles for each user
- ✅ **Real-time Monitoring**: Track host health and resource usage
- ✅ **Load Balancing**: Distribute containers based on host capacity
- ✅ **Security Management**: JWT authentication, API keys, network isolation
- ✅ **Database Persistence**: PostgreSQL for reliable data storage

### API Features
- ✅ **Comprehensive OpenAPI Documentation**: Auto-generated Swagger docs
- ✅ **Authentication Endpoints**: Admin login, key rotation, access management
- ✅ **Host Management**: Registration, monitoring, capacity tracking
- ✅ **Container Operations**: Launch, stop, restart, delete environments
- ✅ **VPN Management**: Profile generation, rotation, revocation
- ✅ **Health Monitoring**: System status and diagnostics

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Machine Lab Manager                      │
├─────────────────────────────────────────────────────────────┤
│  FastAPI Application Server                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │    Auth     │ │   Hosts     │ │ Containers  │            │
│  │     API     │ │     API     │ │     API     │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │    Users    │ │  Security   │ │   Events    │            │
│  │     API     │ │   Module    │ │   System    │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  Database Layer (PostgreSQL)                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │    Users    │ │    Hosts    │ │ Containers  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │  API Keys   │ │ VPN Profiles│                            │
│  └─────────────┘ └─────────────┘                            │
├─────────────────────────────────────────────────────────────┤
│  VPN Server (OpenVPN)                                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │Certificate  │ │   Network   │ │   Client    │            │
│  │ Management  │ │  Isolation  │ │ Provisioning│            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Docker and Docker Compose
- PostgreSQL 12+ (or Docker container)
- OpenVPN server capabilities
- Python 3.8+ (for bare metal deployment)

### Docker Deployment (Recommended)

1. **Clone and Navigate**
   ```bash
   git clone https://github.com/rafliher/machine-lab-platform.git
   cd machine-lab-platform/machine-lab-manager
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env
   ```

3. **Deploy Services**
   ```bash
   docker compose up -d
   ```

4. **Verify Installation**
   ```bash
   curl http://localhost:8000/health
   ```

### Bare Metal Deployment

1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip postgresql-client openvpn
   pip3 install -r requirements.txt
   ```

2. **Setup PostgreSQL Database**
   ```bash
   sudo -u postgres createuser mlab
   sudo -u postgres createdb mlab -O mlab
   sudo -u postgres psql -c "ALTER USER mlab PASSWORD 'your_password';"
   ```

3. **Configure Environment**
   ```bash
   export POSTGRES_HOST=localhost
   export POSTGRES_USER=mlab
   export POSTGRES_PASSWORD=your_password
   export POSTGRES_DB=mlab
   # ... other environment variables
   ```

4. **Initialize Database**
   ```bash
   python3 -c "from app.core.database import create_tables; create_tables()"
   ```

5. **Start Application**
   ```bash
   python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```bash
# Database Configuration
POSTGRES_USER=mlab
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=mlab
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Application Settings
ADMIN_DEFAULT_EMAIL=admin@yourdomain.com
ADMIN_DEFAULT_PASSWORD=your_admin_password
JWT_SECRET=your_jwt_secret_key_minimum_32_characters
ENVIRONMENT=production  # or development

# OpenVPN Configuration
OPENVPN_SERVER_HOST=your.domain.com
OPENVPN_SERVER_PORT=1194
OPENVPN_PROTO=udp
OPENVPN_DEV=tun

# Optional: Cloudflare Integration
USE_CLOUDFLARE=true

# Optional: API Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

### Quick Start

For development setup:

```bash
# 1. Copy environment template
cp .env.sample .env

# 2. Adjust credentials in .env file
nano .env

# 3. Start all services
docker compose up --build

# 4. Access the API
# The manager API will be available at http://localhost:8000/
# API documentation available at http://localhost:8000/api-docs (development mode)
```

### OpenVPN Server Setup

The manager requires an OpenVPN server for VPN functionality:

1. **Initialize OpenVPN**
   ```bash
   sudo ./scripts/init_openvpn.sh
   ```

2. **Configure Server**
   ```bash
   # Edit server configuration
   sudo nano /etc/openvpn/server.conf
   
   # Key settings:
   port 1194
   proto udp
   dev tun
   server 10.8.0.0 255.255.255.0
   push "redirect-gateway def1 bypass-dhcp"
   ```

3. **Start OpenVPN Service**
   ```bash
   sudo systemctl enable openvpn-server@server
   sudo systemctl start openvpn-server@server
   ```

## API Documentation

### Development Mode

When `ENVIRONMENT=development`, access comprehensive API documentation at:
- **Swagger UI**: `http://localhost:8000/api-docs`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Authentication

The API uses two authentication methods:

1. **Admin Key Authentication**: For administrative operations
   ```bash
   # Login to get admin key
   curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@example.com", "password": "password"}'
   
   # Use admin key in headers
   curl -H "X-Admin-Key: your_admin_key" \
     http://localhost:8000/hosts/
   ```

2. **Server Key Authentication**: For host agent communication
   ```bash
   # Host agents use server keys
   curl -H "X-Server-Key: host_server_key" \
     http://localhost:8000/hosts/host-id/heartbeat
   ```

### Core Endpoints

#### Authentication
- `POST /auth/login` - Admin login
- `POST /auth/logout` - Admin logout
- `POST /auth/rotate-key` - Rotate admin key

#### Host Management
- `GET /hosts/` - List all hosts
- `POST /hosts/` - Register new host
- `GET /hosts/{host_id}` - Get host details
- `DELETE /hosts/{host_id}` - Remove host
- `POST /hosts/{host_id}/heartbeat` - Host heartbeat

#### Container Management
- `GET /containers/` - List all containers
- `POST /containers/launch` - Deploy new container
- `GET /containers/{container_id}` - Get container details
- `POST /containers/{container_id}/restart` - Restart container
- `DELETE /containers/{container_id}` - Remove container

#### VPN Management
- `POST /users/vpn` - Generate VPN profile
- `POST /users/vpn/{client_name}/rotate` - Rotate VPN credentials
- `DELETE /users/vpn/{client_name}` - Revoke VPN access

#### System
- `GET /health` - System health check

## Database Schema

The application uses PostgreSQL with the following main tables:

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Hosts Table
```sql
CREATE TABLE hosts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    hostname VARCHAR(255) NOT NULL,
    ip VARCHAR(255) NOT NULL,
    ssh_port INTEGER DEFAULT 22,
    api_port INTEGER DEFAULT 8003,
    max_containers INTEGER DEFAULT 10,
    server_key VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'inactive',
    last_heartbeat TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Containers Table
```sql
CREATE TABLE containers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    host_id UUID REFERENCES hosts(id),
    ip_address VARCHAR(255),
    ports JSONB,
    status VARCHAR(50) DEFAULT 'deploying',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### VPN Profiles Table
```sql
CREATE TABLE vpn_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_name VARCHAR(255) UNIQUE NOT NULL,
    ip_address VARCHAR(255) NOT NULL,
    is_revoked BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## VPN Integration

### OpenVPN Configuration

The manager integrates with OpenVPN to provide secure network access:

1. **Certificate Management**: Automatic generation and revocation of client certificates
2. **IP Assignment**: Dynamic IP allocation from available pool
3. **Network Isolation**: iptables rules for traffic separation
4. **Profile Generation**: Automatic .ovpn file creation

### VPN Profile Format

Generated profiles include:
```
client
dev tun
proto udp
remote your.domain.com 1194
resolv-retry infinite
nobind
persist-key
persist-tun
ca [inline]
cert [inline]
key [inline]
verb 3
```

## Deployment Options

### Docker Compose (Production)

```yaml
version: '3.8'
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: mlab
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: mlab
    volumes:
      - postgres_data:/var/lib/postgresql/data

  manager:
    build: .
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_USER=mlab
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=mlab
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - db
    volumes:
      - /etc/openvpn:/etc/openvpn
      - /var/run/docker.sock:/var/run/docker.sock

volumes:
  postgres_data:
```

### Load Balancer Configuration

For high availability, use a load balancer:

```nginx
upstream siberbox_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 443 ssl;
    server_name api.siberbox.com;
    
    location / {
        proxy_pass http://siberbox_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Monitoring

### Health Endpoints

Monitor application health:

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed system status (with admin key)
curl -H "X-Admin-Key: your_key" \
  http://localhost:8000/system/status
```

### Key Metrics to Monitor

- **Request Rate**: Requests per second
- **Response Time**: Average response time
- **Error Rate**: 4xx/5xx response percentage
- **Host Health**: Number of healthy/unhealthy hosts
- **Container Count**: Active containers per host
- **VPN Connections**: Active VPN sessions

## Troubleshooting

### Common Issues

#### 1. Database Connection Errors

**Symptoms**: Application fails to start with database connection errors

**Solutions**:
```bash
# Check database connectivity
docker exec machine-lab-manager_db_1 psql -U mlab -d mlab -c "SELECT 1;"

# Verify environment variables
docker exec manager env | grep POSTGRES

# Check database logs
docker logs machine-lab-manager_db_1
```

#### 2. VPN Profile Generation Fails

**Symptoms**: VPN endpoint returns errors

**Solutions**:
```bash
# Check OpenVPN service status
sudo systemctl status openvpn-server@server

# Verify certificate authority
sudo ls -la /etc/openvpn/pki/

# Test certificate generation manually
sudo /usr/share/easy-rsa/easyrsa gen-req test-client nopass
```

#### 3. Host Registration Issues

**Symptoms**: Hosts cannot register or send heartbeats

**Solutions**:
```bash
# Check network connectivity from host to manager
curl -H "X-Admin-Key: key" http://manager:8000/hosts/

# Verify server keys in host agent logs
docker logs container-host-agent

# Test host registration manually
curl -X POST "http://manager:8000/hosts/" \
  -H "X-Admin-Key: key" \
  -d '{"hostname": "test", "ip": "192.168.1.100"}'
```

#### 4. Container Deployment Timeouts

**Symptoms**: Container deployments fail with timeout errors

**Solutions**:
```bash
# Check host resources and availability
curl -H "X-Admin-Key: key" http://manager:8000/hosts/

# Monitor deployment logs
docker logs machine-lab-manager_manager_1 -f

# Verify Docker daemon status on host
docker info
```

### Debug Mode

Enable debug logging:

```bash
# Set environment variable
ENVIRONMENT=development
LOG_LEVEL=DEBUG

# Restart container to apply changes
docker compose restart manager
```

### Support Resources

- **API Documentation**: Available at `/api-docs` in development mode
- **GitHub Issues**: [Report bugs and feature requests](https://github.com/rafliher/machine-lab-platform/issues)
- **Main Documentation**: See project root README for overall platform documentation

> **Note**: The Docker Compose configuration is optimized for development environments. Production deployments require additional security hardening, TLS termination, backup strategies, and monitoring solutions.
