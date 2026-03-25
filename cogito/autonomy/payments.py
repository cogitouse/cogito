"""HTTP 402 payment protocol implementation."""

from __future__ import annotations

import logging
from typing import Any

import httpx

from cogito.config.settings import CogitoSettings
from cogito.autonomy.wallet import SolanaWallet

logger = logging.getLogger(__name__)


class PaymentHandler:
    """Handles HTTP 402 Payment Required flows."""

    def __init__(self, settings: CogitoSettings) -> None:
        self.settings = settings
        self.wallet = SolanaWallet(settings)
        self._client = httpx.AsyncClient(timeout=30.0)

    async def request_with_payment(self, url: str, **kwargs: Any) -> httpx.Response:
        """Make an HTTP request, handling 402 responses with automatic payment."""
        response = await self._client.get(url, **kwargs)

        if response.status_code != 402:
            return response

        # extract payment invoice from 402 response
        invoice = self._parse_invoice(response)
        if not invoice:
            logger.error("received 402 but no valid invoice in response")
            raise PaymentError("no invoice in 402 response")

        logger.info(
            "402 received | amount=%.6f SOL | recipient=%s",
            invoice["amount_sol"],
            invoice["recipient"],
        )

        # execute payment
        tx_sig = await self.process_payment(invoice)

        # retry with payment proof
        headers = {
            "X-Payment-Tx": tx_sig,
            "X-Payment-Chain": "solana",
        }
        return await self._client.get(url, headers=headers, **kwargs)

    async def process_payment(self, invoice: dict[str, Any]) -> str:
        """Process a payment invoice by signing and submitting a Solana transaction."""
        recipient = invoice["recipient"]
        amount_sol = invoice["amount_sol"]

        tx_sig = await self.wallet.send_sol(recipient, amount_sol)
        logger.info("payment sent | tx=%s | amount=%.6f SOL", tx_sig, amount_sol)
        return tx_sig

    async def get_cost(self, service: Any) -> float:
        """Get the USD cost for a service renewal."""
        if hasattr(service, "cost_usd"):
            return service.cost_usd
        return 0.0

    def _parse_invoice(self, response: httpx.Response) -> dict[str, Any] | None:
        """Parse a payment invoice from a 402 response."""
        try:
            data = response.json()
            return {
                "recipient": data["payment"]["recipient"],
                "amount_sol": float(data["payment"]["amount"]),
                "amount_usd": float(data["payment"].get("amount_usd", 0)),
                "memo": data["payment"].get("memo", ""),
            }
        except (KeyError, ValueError, Exception):
            return None


class PaymentError(Exception):
    """Raised when a payment flow fails."""
