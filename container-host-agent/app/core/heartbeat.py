import asyncio
import datetime
import logging

import httpx
import psutil
from docker import DockerClient

from app.core.config import settings

logger = logging.getLogger("heartbeat")
docker = DockerClient(base_url=settings.docker_socket)


async def heartbeat_loop():
    url = f"{settings.manager_url.rstrip('/')}/hosts/{settings.host_id}/heartbeat"
    headers = {"X-Server-Key": settings.server_key}

    async with httpx.AsyncClient() as client:
        while True:
            # gather stats
            try:
                cpu = psutil.cpu_percent(interval=None)
                mem = psutil.virtual_memory().percent
                containers = len(docker.containers.list())

            except Exception as e:
                logger.error("Failed to gather stats: %s", e)
                cpu = 0
                mem = 0
                containers = 0

            payload = {
                "cpu": int(cpu),
                "mem": int(mem),
                "containers": containers,
            }

            # send heartbeat
            try:
                resp = await client.post(
                    url, json=payload, headers=headers, timeout=5.0
                )
                resp.raise_for_status()
                logger.debug("Heartbeat ack: %s", resp.json())
            except httpx.HTTPStatusError as e:
                # Server returned a non-2xx status
                status = e.response.status_code
                body = e.response.text
                logger.warning(
                    "Heartbeat failed: HTTP %s – response body: %s", status, body
                )
            except httpx.RequestError as e:
                # Network problem, timeout, DNS error, etc.
                logger.warning("Heartbeat request error: %s", e)
            except Exception as e:
                # Anything else
                logger.warning("Heartbeat failed: %s", e)

            await asyncio.sleep(settings.heartbeat_interval)
