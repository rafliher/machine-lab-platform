# Machine‑Lab Manager (Base Skeleton)

This is a **minimal FastAPI-based skeleton** for the *Machine‑Lab Manager* control-plane, as described in the project spec.

## Components spun up by `docker-compose`

| Service | Image | Purpose |
|---------|-------|---------|
| `db` | `postgres:16` | Primary PostgreSQL store |
| `vpn` | `linuxserver/wireguard:latest` | WireGuard hub (admin + user tunnels) |
| `mq` | `rabbitmq:3-management` | Message queue for placement events |
| `manager` | *local build* | REST/gRPC API + scheduler |
| `grafana` | `grafana/grafana:latest` | (optional) monitoring UI |
| `prometheus` | `prom/prometheus:latest` | (optional) metrics store |

> **Note**: The Compose file is aimed at a **development** environment (single‑node). Production will require hardened images, storage mounts, backups, and TLS termination.

## Quick start

```bash
cp .env.sample .env       # adjust credentials
docker compose up --build
```

The manager API will be available at <http://localhost:8000/docs> (Swagger).
