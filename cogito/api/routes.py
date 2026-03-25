"""API route definitions."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from cogito.config.settings import CogitoSettings


class EvalRequest(BaseModel):
    model_id: str
    dimensions: list[str] | None = None


class EvalResponse(BaseModel):
    model_id: str
    cogito_score: float
    dimension_scores: dict[str, float]


class HealthResponse(BaseModel):
    status: str
    version: str


def build_router(settings: CogitoSettings) -> APIRouter:
    router = APIRouter()

    @router.get("/health", response_model=HealthResponse)
    async def health():
        from cogito import __version__
        return HealthResponse(status="ok", version=__version__)

    @router.post("/evaluate", response_model=EvalResponse)
    async def evaluate(req: EvalRequest):
        from cogito.eval.runner import EvaluationRunner

        runner = EvaluationRunner(settings)
        try:
            result = await runner.run(
                model_id=req.model_id, dimensions=req.dimensions
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return EvalResponse(
            model_id=result.model_id,
            cogito_score=round(result.cogito_score, 2),
            dimension_scores={
                k: round(v, 2) for k, v in result.dimension_scores.items()
            },
        )

    @router.get("/wallet/balance")
    async def wallet_balance():
        from cogito.autonomy.wallet import SolanaWallet
        wallet = SolanaWallet(settings)
        await wallet.connect()
        balance = await wallet.get_balance()
        return {
            "address": settings.solana_wallet_address,
            "balance_sol": balance,
        }

    return router
