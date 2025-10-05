# SiberBox: Containerized Cybersecurity Learning Platform

## Table of Contents
1. [Project Description](#project-description)
2. [Installation Guide](#installation-guide)
3. [Usage Guide](#usage-guide)

---

## Project Description

### Overview

SiberBox is a comprehensive containerized cybersecurity learning platform that provides isolated, VPN-secured environments for hands-on security training and research. The platform enables instructors and researchers to deploy complex multi-container scenarios with automatic VPN integration, ensuring secure access while maintaining complete network isolation between users.

### Key Features

- **Dynamic Container Orchestration**: Full Docker Compose support for complex multi-service environments
- **Automatic VPN Integration**: Dynamic OpenVPN profile generation and traffic routing
- **Real-time Monitoring**: Host health and resource usage tracking across distributed infrastructure
- **RESTful API**: Comprehensive programmatic environment management
- **Web Administration**: Dashboard interface with Swagger API documentation
- **Security-First Design**: Complete network isolation and automatic cleanup

### Target Audience

The platform addresses the critical need for scalable, secure cybersecurity education infrastructure that can accommodate diverse learning scenarios:

- **Academic Institutions**: Universities and colleges teaching cybersecurity courses
- **Training Organizations**: Professional cybersecurity certification providers
- **Security Researchers**: Individual researchers requiring isolated lab environments
- **Corporate Training**: Enterprise security awareness and hands-on training programs

### Use Cases

- **Basic Penetration Testing Labs**: Controlled environments for learning ethical hacking
- **Advanced Red Team Exercises**: Complex multi-stage attack simulation scenarios
- **Vulnerability Research**: Isolated environments for malware analysis and reverse engineering
- **Network Security Training**: Hands-on experience with firewalls, IDS/IPS, and network monitoring
- **Incident Response Training**: Realistic scenarios for practicing digital forensics

### Technical Architecture

#### Backend Infrastructure
- **API Server**: FastAPI (Python) with PostgreSQL database for scalable, async operations
- **Container Management**: Docker & Docker Compose orchestration for complex service deployments
- **VPN Integration**: OpenVPN with dynamic client certificate generation and automatic provisioning
- **Network Security**: iptables-based traffic isolation and routing for complete user separation
- **Authentication**: JWT-based admin authentication with API key management
- **Monitoring**: Real-time host health and resource usage tracking

#### Core Components

1. **Machine Lab Manager**
   - Central API server for environment orchestration
   - Database management for users, hosts, containers, and VPN profiles
   - Automatic resource allocation and load balancing
   - Security policy enforcement and audit logging

2. **Container Host Agent**
   - Distributed agents for container lifecycle management
   - Real-time resource monitoring and reporting
   - Local Docker Compose execution and management
   - Secure communication with central manager

3. **VPN Server**
   - Integrated OpenVPN server with automatic client provisioning
   - Dynamic certificate generation and revocation
   - Network traffic routing and isolation
   - Automatic cleanup on environment termination

4. **Web Interface**
   - Administrative dashboard for platform management
   - Swagger API documentation for developers
   - Real-time monitoring and status displays
   - User-friendly environment deployment interface

#### Deployment Features

- **Multi-Host Distribution**: Automatic container placement across multiple physical hosts
- **Load Balancing**: Resource-aware container placement and capacity management
- **Auto-Scaling**: Dynamic resource allocation based on demand
- **High Availability**: Fault-tolerant design with automatic failover capabilities
- **Security Cleanup**: Complete environment teardown with certificate revocation

#### Security Features

- **Individual VPN Profiles**: Unique OpenVPN configurations per user and container
- **Network Segmentation**: iptables-based traffic isolation between environments
- **Certificate Management**: Automatic SSL/TLS certificate generation and cleanup
- **Authentication**: Multi-layer security with admin keys and server authentication
- **Audit Logging**: Comprehensive logging of all platform activities
- **Zero-Trust Network**: Default-deny network policies with explicit allow rules

### Architecture Design

The platform follows a microservices architecture designed for scalability and security:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Interface │    │  External APIs  │    │   Admin Tools   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Machine Lab     │
                    │ Manager (API)   │
                    └─────────┬───────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │ Container   │ │ Container   │ │ Container   │
    │ Host Agent 1│ │ Host Agent 2│ │ Host Agent N│
    └─────────────┘ └─────────────┘ └─────────────┘
```

### Integration Capabilities

SiberBox is designed as a microservice engine for machine lab orchestration, intended to be integrated with larger educational platforms:

- **API-First Design**: RESTful API enables integration with existing Learning Management Systems (LMS)
- **Webhook Support**: Real-time notifications for environment state changes
- **SSO Integration**: Compatible with SAML, OAuth, and other enterprise authentication systems
- **Gradebook Integration**: Automatic scoring and progress tracking capabilities
- **Multi-Tenant Architecture**: Support for multiple organizations and user groups

### Example Integrations

- **akademi.siberlab.id**: Comprehensive cybersecurity education platform
- **University LMS**: Direct integration with Moodle, Canvas, or Blackboard
- **Corporate Training Platforms**: Enterprise security awareness programs
- **SIEM Training**: Integration with security operations center (SOC) training modules

---

## Installation Guide

### Prerequisites

#### System Requirements

**Manager Server:**
- Ubuntu 20.04+ or similar Linux distribution
- 4+ CPU cores, 8GB+ RAM, 100GB+ storage
- Docker and Docker Compose
- PostgreSQL 12+ or container equivalent
- Public IP address or domain name for VPN access

**Container Host(s):**
- Ubuntu 20.04+ or similar Linux distribution
- 8+ CPU cores, 16GB+ RAM, 500GB+ storage
- Docker and Docker Compose
- Network connectivity to Manager Server

#### Software Dependencies

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install additional utilities
sudo apt install -y git python3 python3-pip postgresql-client
```

### Installation Steps

#### 1. Clone Repository

```bash
git clone https://github.com/rafliher/machine-lab-platform.git
cd machine-lab-platform
```

#### 2. Manager Server Setup

```bash
cd machine-lab-manager

# Configure environment variables
cp .env.example .env
nano .env
```

**Configure `.env` file:**
```bash
# PostgreSQL Configuration
POSTGRES_USER=mlab
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=mlab
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Manager Application
ADMIN_DEFAULT_EMAIL=admin@yourdomain.com
ADMIN_DEFAULT_PASSWORD=your_admin_password
JWT_SECRET=your_jwt_secret_key

# Environment
ENVIRONMENT=production

# OpenVPN Configuration
OPENVPN_SERVER_HOST=your.domain.com
OPENVPN_SERVER_PORT=1194
OPENVPN_PROTO=udp
OPENVPN_DEV=tun
```

#### 3. Deploy Manager Services

```bash
# Start the manager and database
docker-compose up -d

# Verify services are running
docker-compose logs -f

# Check service health
curl http://localhost:8000/health
```

#### 4. Container Host Agent Setup

On each container host machine:

```bash
cd container-host-agent

# Configure environment
cp .env.example .env
nano .env
```

**Configure agent `.env` file:**
```bash
# Shared secret (same as manager's JWT_SECRET)
JWT_SECRET=your_jwt_secret_key

# Docker socket
DOCKER_SOCKET=unix:///var/run/docker.sock

# Manager connection
MANAGER_URL=https://your-manager-domain.com
HOST_ID=generate_uuid_here
SERVER_KEY=will_be_provided_after_registration
HEARTBEAT_INTERVAL=10
```

#### 5. Register Container Hosts

Use the Manager API to register each container host:

```bash
# Login to get admin key
curl -X POST "https://your-manager-domain.com/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@yourdomain.com",
    "password": "your_admin_password"
  }'

# Register host (save the returned host_id and server_key)
curl -X POST "https://your-manager-domain.com/hosts/" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: your_admin_key_from_login" \
  -d '{
    "hostname": "host-01",
    "ip": "host-ip-address",
    "ssh_port": 22,
    "api_port": 8003,
    "max_containers": 10
  }'
```

#### 6. Start Container Host Agents

Update the agent `.env` file with the registration details:

```bash
# Update .env with registration details
HOST_ID=uuid_from_registration
SERVER_KEY=server_key_from_registration

# Start the agent
docker-compose up -d

# Verify agent is running and connecting
docker-compose logs -f
```

#### 7. Web Interface Setup (Optional)

```bash
cd machine-lab-platform-ui

# Configure API endpoint
echo "VUE_APP_API_BASE_URL=https://your-manager-domain.com/" > .env

# Build and deploy
npm install
npm run build

# Serve the built files (using nginx, apache, or static hosting)
```

### SSL/TLS Configuration

#### Option 1: Using Cloudflare (Recommended)

1. Point your domain to your server IP in Cloudflare DNS
2. Enable Cloudflare proxy (orange cloud)
3. Set SSL/TLS mode to "Full" or "Full (strict)"
4. Enable "Always Use HTTPS"

#### Option 2: Using Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Generate certificate
sudo certbot --nginx -d your-manager-domain.com

# Configure nginx reverse proxy
sudo nano /etc/nginx/sites-available/siberbox
```

**Nginx configuration:**
```nginx
server {
    listen 443 ssl;
    server_name your-manager-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-manager-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-manager-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Verification

Test your installation:

```bash
# Check manager health
curl https://your-manager-domain.com/health

# List registered hosts
curl -H "X-Admin-Key: your_admin_key" \
  https://your-manager-domain.com/hosts/

# Test container deployment (using example zip)
curl -X POST "https://your-manager-domain.com/containers/launch" \
  -H "X-Admin-Key: your_admin_key" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -F "file=@example/pug_is_a_blind_dog.zip"
```

---

## Usage Guide

### Getting Started

#### 1. Administrative Access

Access the API documentation at `https://your-domain.com/docs` (development mode) or use the API directly.

**Login to get admin key:**
```bash
curl -X POST "https://your-domain.com/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@yourdomain.com",
    "password": "your_admin_password"
  }'
```

Save the returned `admin_key` for subsequent API calls.

#### 2. Host Management

**List all hosts:**
```bash
curl -H "X-Admin-Key: your_admin_key" \
  https://your-domain.com/hosts/
```

**Register new host:**
```bash
curl -X POST "https://your-domain.com/hosts/" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: your_admin_key" \
  -d '{
    "hostname": "host-02",
    "ip": "192.168.1.100",
    "ssh_port": 22,
    "api_port": 8003,
    "max_containers": 20
  }'
```

### Container Environment Deployment

#### 1. Prepare Lab Environment

Create a ZIP file containing:
- `docker-compose.yml` or `docker-compose.yaml`
- All referenced files (Dockerfiles, scripts, configs)
- Any additional resources needed by containers

**Example structure:**
```
lab-environment.zip
├── docker-compose.yml
├── Dockerfile
├── src/
│   ├── app.py
│   └── requirements.txt
└── config/
    └── nginx.conf
```

**Sample docker-compose.yml:**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "80:80"
    volumes:
      - ./src:/app
    environment:
      - DEBUG=true
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: testdb
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

#### 2. Deploy Environment

**Launch container environment:**
```bash
curl -X POST "https://your-domain.com/containers/launch" \
  -H "X-Admin-Key: your_admin_key" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -F "file=@lab-environment.zip"
```

Response includes:
- `id`: Container environment ID
- `host_id`: Host where environment is deployed

#### 3. Environment Management

**List all containers:**
```bash
curl -H "X-Admin-Key: your_admin_key" \
  https://your-domain.com/containers/
```

**Get container details:**
```bash
curl -H "X-Admin-Key: your_admin_key" \
  https://your-domain.com/containers/{container_id}
```

**Restart container:**
```bash
curl -X POST "https://your-domain.com/containers/{container_id}/restart" \
  -H "X-Admin-Key: your_admin_key"
```

**Stop and remove container:**
```bash
curl -X DELETE "https://your-domain.com/containers/{container_id}" \
  -H "X-Admin-Key: your_admin_key"
```

### VPN Access Management

#### 1. Generate User VPN Profile

```bash
curl -X POST "https://your-domain.com/users/vpn" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: your_admin_key" \
  -d '{
    "client_name": "user123"
  }' --output user123.ovpn
```

#### 2. VPN Profile Management

**Rotate VPN credentials:**
```bash
curl -X POST "https://your-domain.com/users/vpn/user123/rotate" \
  -H "X-Admin-Key: your_admin_key" --output user123-new.ovpn
```

#### 3. Accessing Deployed Environments

1. **Download VPN profile** for the user
2. **Import profile** into OpenVPN client
3. **Connect to VPN**
4. **Get container details** to obtain assigned IP address
5. **Access environment** via container IP

### Example Workflow

#### Complete Lab Deployment Example

```bash
# 1. Login
ADMIN_KEY=$(curl -s -X POST "https://your-domain.com/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@yourdomain.com",
    "password": "your_admin_password"
  }' | jq -r '.admin_key')

# 2. Generate user VPN profile
curl -X POST "https://your-domain.com/users/vpn" \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: $ADMIN_KEY" \
  -d '{"client_name": "student001"}' \
  --output student001.ovpn

# 3. Deploy lab environment
DEPLOYMENT=$(curl -s -X POST "https://your-domain.com/containers/launch" \
  -H "X-Admin-Key: $ADMIN_KEY" \
  -F "user_id=550e8400-e29b-41d4-a716-446655440000" \
  -F "file=@penetration-testing-lab.zip")

CONTAINER_ID=$(echo $DEPLOYMENT | jq -r '.id')

# 4. Wait for deployment and get access details
sleep 30
curl -H "X-Admin-Key: $ADMIN_KEY" \
  "https://your-domain.com/containers/$CONTAINER_ID" \
  | jq '.ip_address'

# 5. Student connects to VPN and accesses lab at returned IP
```

### Monitoring and Maintenance

#### 1. System Health Monitoring

**Check overall system health:**
```bash
curl https://your-domain.com/health
```

**Monitor host status:**
```bash
curl -H "X-Admin-Key: your_admin_key" \
  https://your-domain.com/hosts/ | jq '.[] | {hostname, status, cpu_percent, mem_percent, current_containers}'
```

#### 2. Resource Management

**Check host capacity:**
```bash
# View host resource utilization
curl -H "X-Admin-Key: your_admin_key" \
  https://your-domain.com/hosts/ | jq '.[] | select(.cpu_percent > 80 or .mem_percent > 80)'
```

**Container cleanup:**
```bash
# List long-running containers
curl -H "X-Admin-Key: your_admin_key" \
  https://your-domain.com/containers/ | jq '.[] | select(.created_at < "2024-01-01")'
```

### Security Best Practices

#### 1. API Key Management

- **Rotate admin keys** regularly using `/auth/rotate-key`
- **Use environment-specific keys** for different deployments
- **Monitor API access** through application logs

#### 2. VPN Security

- **Rotate VPN profiles** for long-term users
- **Monitor VPN connections** through OpenVPN logs
- **Revoke access** immediately when users no longer need access

#### 3. Container Security

- **Scan container images** before deployment
- **Limit container resources** to prevent resource exhaustion
- **Monitor container behavior** for suspicious activity

### Troubleshooting

#### Common Issues

**1. Container deployment fails:**
```bash
# Check host availability
curl -H "X-Admin-Key: your_admin_key" \
  https://your-domain.com/hosts/ | jq '.[] | select(.status == "healthy")'

# Check host capacity
curl -H "X-Admin-Key: your_admin_key" \
  https://your-domain.com/hosts/ | jq '.[] | select(.current_containers < .max_containers)'
```

**2. VPN connectivity issues:**
```bash
# Check VPN server status
sudo systemctl status openvpn-server@server

# Check VPN logs
sudo journalctl -u openvpn-server@server -f

# Test VPN configuration
sudo openvpn --config /etc/openvpn/client.ovpn --verb 4
```

**3. Host agent disconnection:**
```bash
# Check agent logs
docker-compose logs container-host-agent

# Test manager connectivity
curl -H "X-Server-Key: your_server_key" \
  https://your-domain.com/hosts/your-host-id/heartbeat \
  -d '{"cpu": 10, "mem": 20, "containers": 1}'
```

### Integration Examples

#### 1. LMS Integration

**Moodle Plugin Example:**
```php
// Deploy lab for student
$deployment = api_call('POST', '/containers/launch', [
    'user_id' => $student->uuid,
    'file' => $lab_package
]);

// Store deployment ID in gradebook
$DB->insert_record('siberbox_deployments', [
    'userid' => $student->id,
    'courseid' => $course->id,
    'container_id' => $deployment['id'],
    'created' => time()
]);
```

#### 2. Automated Scoring

**Progress Tracking:**
```python
import requests

def check_student_progress(container_id, admin_key):
    # Get container details
    response = requests.get(
        f"https://your-domain.com/containers/{container_id}",
        headers={"X-Admin-Key": admin_key}
    )
    
    container_ip = response.json()['ip_address']
    
    # Check specific objectives
    objectives = [
        check_web_service(container_ip),
        check_database_access(container_ip),
        check_security_scan(container_ip)
    ]
    
    return sum(objectives) / len(objectives) * 100
```

### Advanced Configuration

#### 1. Multi-Tenant Setup

Configure different user groups with isolated resources:

```bash
# Create organization-specific hosts
curl -X POST "https://your-domain.com/hosts/" \
  -H "X-Admin-Key: your_admin_key" \
  -d '{
    "hostname": "org1-host-01",
    "ip": "10.1.1.100",
    "max_containers": 10,
    "tags": ["organization:org1"]
  }'
```

#### 2. Custom Network Policies

Implement advanced network isolation:

```bash
# Configure iptables rules for specific scenarios
sudo iptables -A FORWARD -s 10.8.0.0/24 -d 192.168.1.0/24 -j DROP
sudo iptables -A FORWARD -s 10.8.0.0/24 -d 10.8.0.0/24 -j ACCEPT
```

#### 3. Automated Backups

Set up regular backups of critical data:

```bash
#!/bin/bash
# Backup script
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
docker exec machine-lab-manager_db_1 pg_dump -U mlab mlab > backup_${DATE}.sql

# Backup VPN configurations
tar -czf vpn_backup_${DATE}.tar.gz /etc/openvpn/

# Upload to remote storage
aws s3 cp backup_${DATE}.sql s3://your-backup-bucket/
aws s3 cp vpn_backup_${DATE}.tar.gz s3://your-backup-bucket/
```
