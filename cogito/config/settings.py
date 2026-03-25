"""Configuration loader for Cogito."""

from __future__ import annotations

import os
import logging
from pathlib import Path
from typing import Optional

import toml
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class AgentConfig(BaseModel):
    name: str = "cogito"
    cycle_interval_ms: int = 2000
    max_actions_per_cycle: int = 10
    memory_capacity_tokens: int = 200_000


class ReasoningConfig(BaseModel):
    model: str = "gpt-4-turbo"
    temperature: float = 0.3
    max_tokens: int = 4096
    chain_of_thought: bool = True


class EvaluationConfig(BaseModel):
    dimensions: list[str] = Field(default_factory=lambda: [
        "self_awareness",
        "theory_of_mind",
        "metacognition",
        "causal_reasoning",
        "creative_divergence",
        "long_horizon_planning",
        "world_modeling",
    ])
    probes_per_dimension: int = 50
    scoring_method: str = "weighted_composite"
    gpu_accelerated: bool = True


class ConsciousnessConfig(BaseModel):
    probe_depth: int = 3
    mapping_resolution: int = 100
    confidence_threshold: float = 0.85


class AutonomyConfig(BaseModel):
    enabled: bool = True
    payment_protocol: str = "402"
    self_sustain: bool = True
    budget_limit_usd: float = 100.0


class APIConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8420
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])


class VisualizationConfig(BaseModel):
    output_dir: str = "reports"
    format: str = "svg"


class CogitoSettings(BaseModel):
    agent: AgentConfig = Field(default_factory=AgentConfig)
    reasoning: ReasoningConfig = Field(default_factory=ReasoningConfig)
    evaluation: EvaluationConfig = Field(default_factory=EvaluationConfig)
    consciousness: ConsciousnessConfig = Field(default_factory=ConsciousnessConfig)
    autonomy: AutonomyConfig = Field(default_factory=AutonomyConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    visualization: VisualizationConfig = Field(default_factory=VisualizationConfig)

    # env-loaded secrets
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    xai_grok_api_key: Optional[str] = None
    solana_rpc_url: str = "https://api.mainnet-beta.solana.com"
    solana_wallet_address: Optional[str] = None
    solana_wallet_private_key: Optional[str] = None


def load_settings(config_path: str | Path | None = None) -> CogitoSettings:
    """Load settings from TOML config and environment variables."""
    path = Path(config_path) if config_path else Path("config/cogito.toml")
    data: dict = {}
    if path.exists():
        data = toml.load(path)
        logger.info("loaded config from %s", path)
    else:
        logger.warning("config file not found at %s, using defaults", path)

    settings = CogitoSettings(**data)

    # overlay environment variables
    settings.openai_api_key = os.getenv("OPENAI_API_KEY")
    settings.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    settings.xai_grok_api_key = os.getenv("XAI_GROK_API_KEY")
    settings.solana_rpc_url = os.getenv(
        "SOLANA_RPC_URL", settings.solana_rpc_url
    )
    settings.solana_wallet_address = os.getenv("SOLANA_WALLET_ADDRESS")
    settings.solana_wallet_private_key = os.getenv("SOLANA_WALLET_PRIVATE_KEY")

    return settings
