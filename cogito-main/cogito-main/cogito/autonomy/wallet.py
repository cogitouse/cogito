"""Solana wallet operations."""

from __future__ import annotations

import logging
from typing import Optional

from cogito.config.settings import CogitoSettings

logger = logging.getLogger(__name__)


class SolanaWallet:
    """Manages Solana wallet for autonomous transactions."""

    def __init__(self, settings: CogitoSettings) -> None:
        self.rpc_url = settings.solana_rpc_url
        self.address = settings.solana_wallet_address
        self._private_key = settings.solana_wallet_private_key
        self._client: Optional[object] = None

    async def connect(self) -> None:
        """Establish connection to Solana RPC."""
        from solana.rpc.async_api import AsyncClient

        self._client = AsyncClient(self.rpc_url)
        logger.info("wallet connected to %s", self.rpc_url)

    async def get_balance(self) -> float:
        """Get wallet balance in SOL."""
        if not self._client or not self.address:
            return 0.0

        from solders.pubkey import Pubkey

        pubkey = Pubkey.from_string(self.address)
        resp = await self._client.get_balance(pubkey)
        lamports = resp.value
        return lamports / 1_000_000_000

    async def send_sol(self, recipient: str, amount_sol: float) -> str:
        """Send SOL to a recipient address. Returns transaction signature."""
        if not self._client or not self._private_key:
            raise WalletError("wallet not initialized or missing private key")

        from solders.pubkey import Pubkey
        from solders.keypair import Keypair
        from solders.system_program import transfer, TransferParams
        from solana.transaction import Transaction

        sender_kp = Keypair.from_base58_string(self._private_key)
        recipient_pk = Pubkey.from_string(recipient)
        lamports = int(amount_sol * 1_000_000_000)

        ix = transfer(TransferParams(
            from_pubkey=sender_kp.pubkey(),
            to_pubkey=recipient_pk,
            lamports=lamports,
        ))

        tx = Transaction().add(ix)
        resp = await self._client.send_transaction(tx, sender_kp)
        sig = str(resp.value)
        logger.info("sent %.6f SOL to %s | sig=%s", amount_sol, recipient, sig)
        return sig


class WalletError(Exception):
    """Raised when wallet operations fail."""
