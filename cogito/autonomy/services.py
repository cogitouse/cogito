"""Internet service registry for autonomous resource management."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ServiceEntry:
    name: str
    endpoint: str
    cost_usd: float = 0.0
    expires_at: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def needs_renewal(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) >= self.expires_at - timedelta(hours=1)

    async def request_invoice(self) -> dict[str, Any]:
        """Request a payment invoice from the service."""
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.endpoint}/invoice",
                json={"service": self.name},
            )
            return resp.json()


class ServiceRegistry:
    """Registry of services the agent interacts with."""

    def __init__(self) -> None:
        self._services: dict[str, ServiceEntry] = {}

    def register(self, service: ServiceEntry) -> None:
        self._services[service.name] = service
        logger.info("registered service: %s at %s", service.name, service.endpoint)

    def unregister(self, name: str) -> None:
        self._services.pop(name, None)

    def get(self, name: str) -> ServiceEntry | None:
        return self._services.get(name)

    def list_active(self) -> list[ServiceEntry]:
        return list(self._services.values())

    def list_expiring(self, within_hours: int = 24) -> list[ServiceEntry]:
        cutoff = datetime.now(timezone.utc) + timedelta(hours=within_hours)
        return [
            s for s in self._services.values()
            if s.expires_at and s.expires_at <= cutoff
        ]
