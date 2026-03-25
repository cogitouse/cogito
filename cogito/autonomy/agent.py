"""Self-sustaining agent controller."""

from __future__ import annotations

import logging
from typing import Any

from cogito.config.settings import CogitoSettings
from cogito.autonomy.wallet import SolanaWallet
from cogito.autonomy.payments import PaymentHandler
from cogito.autonomy.services import ServiceRegistry

logger = logging.getLogger(__name__)


class SelfSustainController:
    """Manages autonomous resource acquisition and payment flows."""

    def __init__(self, settings: CogitoSettings) -> None:
        self.settings = settings
        self.wallet = SolanaWallet(settings)
        self.payments = PaymentHandler(settings)
        self.services = ServiceRegistry()
        self._budget_spent_usd = 0.0

    async def initialize(self) -> None:
        """Initialize wallet connection and service registry."""
        await self.wallet.connect()
        balance = await self.wallet.get_balance()
        logger.info(
            "self-sustain initialized | wallet=%s | balance=%.4f SOL",
            self.settings.solana_wallet_address,
            balance,
        )

    async def check_resources(self) -> dict[str, Any]:
        """Check resource levels and acquire more if needed."""
        status = {
            "balance_sol": await self.wallet.get_balance(),
            "budget_spent_usd": self._budget_spent_usd,
            "budget_limit_usd": self.settings.autonomy.budget_limit_usd,
        }

        if self._budget_spent_usd >= self.settings.autonomy.budget_limit_usd:
            logger.warning("budget limit reached, pausing autonomous spending")
            return {**status, "action": "paused"}

        # check if any registered services need renewal
        for service in self.services.list_active():
            if service.needs_renewal():
                cost = await self.payments.get_cost(service)
                if self._can_afford(cost):
                    await self._renew_service(service)

        return {**status, "action": "ok"}

    def _can_afford(self, cost_usd: float) -> bool:
        remaining = self.settings.autonomy.budget_limit_usd - self._budget_spent_usd
        return cost_usd <= remaining

    async def _renew_service(self, service: Any) -> None:
        """Renew a service via 402 payment."""
        try:
            invoice = await service.request_invoice()
            tx_sig = await self.payments.process_payment(invoice)
            self._budget_spent_usd += invoice.get("amount_usd", 0.0)
            logger.info("renewed service %s | tx=%s", service.name, tx_sig)
        except Exception as exc:
            logger.error("failed to renew %s: %s", service.name, exc)
