# Machine‑Lab Manager

This is a **minimal FastAPI-based skeleton** for the *Machine‑Lab Manager* control-plane, as described in the project spec.

> **Note**: The Compose file is aimed at a **development** environment (single‑node). Production will require hardened images, storage mounts, backups, and TLS termination.

## Quick start

```bash
cp .env.sample .env       # adjust credentials
docker compose up --build
```

The manager API will be available at <http://localhost:8000/>
