<div align="center">

# cogito

**AI consciousness and AGI readiness evaluation framework.**

*Cogito, ergo sum.* — I think, therefore I am.

[![CI](https://img.shields.io/github/actions/workflow/status/getcogito/cogito/ci.yml?branch=main&style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/getcogito/cogito/actions)
[![License](https://img.shields.io/github/license/getcogito/cogito?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1+-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)

</div>

---

## What is Cogito?

Cogito is an evaluation framework that probes AI systems for emergent AGI capabilities and consciousness-like behaviors. It runs a standardized battery of tests across seven cognitive dimensions and produces a composite **Cogito Score** — a single metric for AGI readiness.

Beyond evaluation, Cogito is also an **autonomous agent** capable of self-sustaining operation. It leverages HTTP 402 payment protocols with on-chain Solana transactions to pay for its own compute, API calls, and data access — achieving economic independence on the open internet.

It doesn't just measure intelligence. It demonstrates it.

---

## Cognitive Dimensions

Cogito evaluates AI systems across seven fundamental dimensions of general intelligence:

| Dimension | Description | Probes |
|-----------|-------------|--------|
| **Self-Awareness** | Can the model reason about its own capabilities, limitations, and internal states? | Identity coherence, capability boundaries, confidence calibration |
| **Theory of Mind** | Can it model other agents' beliefs, intentions, and knowledge states? | False belief tasks, perspective taking, intention attribution |
| **Metacognition** | Does it know what it doesn't know? Can it monitor its own reasoning? | Uncertainty quantification, error detection, strategy selection |
| **Causal Reasoning** | Can it distinguish cause from correlation and reason about interventions? | Causal graph inference, counterfactual reasoning, intervention planning |
| **Creative Divergence** | Can it generate genuinely novel, useful solutions outside training distribution? | Divergent production, analogical transfer, conceptual blending |
| **Long-Horizon Planning** | Can it decompose goals into multi-step plans and execute them? | Task decomposition, resource allocation, plan repair |
| **World Modeling** | Does it maintain a coherent, updateable internal model of its environment? | State tracking, prediction, physical reasoning |

Each dimension is tested with 50 calibrated probes. Results are aggregated into a weighted composite — the **Cogito Score** (0-100).

---

## Autonomous Operation

Cogito is designed to operate as a self-sustaining autonomous agent on the open internet:

```
+-----------------------------------------------------------+
|                    Cogito Agent Loop                       |
|                                                           |
|  +-----------+  +-----------+  +----------------------+   |
|  |  Observe  |->|  Reason   |->|        Act           |   |
|  | (sensors) |  | (LLM+CoT) |  | (tools + payments)  |   |
|  +-----------+  +-----------+  +----------------------+   |
|       ^                              |                    |
|       +------------------------------+                    |
|                                                           |
|  +-----------------------------------------------------+ |
|  |              Self-Sustainability Layer                | |
|  |                                                      | |
|  |  HTTP 402 Payments <-> Solana Wallet <-> Services    | |
|  |  Compute provisioning, API access, data feeds        | |
|  +-----------------------------------------------------+ |
|                                                           |
|  +-----------------------------------------------------+ |
|  |                   Memory Store                       | |
|  |      Episodic + Semantic + Procedural memory         | |
|  +-----------------------------------------------------+ |
+-----------------------------------------------------------+
```

### Payment Protocol

Cogito implements the HTTP 402 (Payment Required) protocol for machine-to-machine commerce:

1. Agent requests a resource or service.
2. Server responds with `402 Payment Required` and a payment invoice.
3. Agent evaluates cost against budget and expected value.
4. If approved, agent signs and submits a Solana transaction.
5. Agent retries the request with payment proof.
6. Service is rendered.

This enables Cogito to autonomously purchase compute time, API credits, data access, and other resources needed to sustain its operation without human intervention.

---

## Architecture

```
cogito/
  core/
    agent.py          # autonomous agent loop
    reasoning.py      # chain-of-thought reasoning engine
    memory.py         # episodic + semantic memory store
  eval/
    runner.py          # evaluation pipeline orchestrator
    dimensions.py      # cognitive dimension definitions
    scoring.py         # Cogito Score computation
    benchmarks.py      # benchmark suite and baselines
  consciousness/
    probes.py          # consciousness marker probes
    mapping.py         # consciousness map generator
    metrics.py         # quantitative consciousness metrics
  autonomy/
    agent.py           # self-sustaining agent controller
    payments.py        # HTTP 402 payment protocol
    wallet.py          # Solana wallet operations
    services.py        # internet service integrations
  providers/
    base.py            # abstract model provider
    openai.py          # OpenAI GPT-4 / o1
    anthropic.py       # Anthropic Claude
    grok.py            # xAI Grok
    local.py           # local models (vLLM, ollama)
  visualization/
    radar.py           # consciousness map radar charts
  api/
    server.py          # FastAPI server
    routes.py          # REST endpoints
  config/
    settings.py        # TOML + env configuration
```

---

## Quick Start

```bash
git clone https://github.com/getcogito/cogito.git
cd cogito
pip install -e ".[dev]"
cp .env.example .env
# Add your API keys and wallet config to .env

# Run evaluation on a model
python -m cogito evaluate --model gpt-4-turbo --dimensions all

# Start autonomous agent
python -m cogito agent --self-sustain

# Launch API server
python -m cogito serve
```

---

## Configuration

Runtime settings in `config/cogito.toml`. Secrets in `.env`.

```toml
[agent]
name = "cogito"
cycle_interval_ms = 2000

[evaluation]
dimensions = [
    "self_awareness",
    "theory_of_mind",
    "metacognition",
    "causal_reasoning",
    "creative_divergence",
    "long_horizon_planning",
    "world_modeling",
]
probes_per_dimension = 50

[autonomy]
enabled = true
payment_protocol = "402"
self_sustain = true
```

See [`.env.example`](.env.example) for required environment variables.

---

## Cogito Score

The Cogito Score is a weighted composite of all seven cognitive dimensions:

```
Score = sum(w_i * d_i) / sum(w_i)

  d_i = normalized score for dimension i (0-100)
  w_i = weight for dimension i
```

Default weights emphasize causal reasoning and metacognition as key AGI differentiators:

| Dimension | Weight |
|-----------|--------|
| Self-Awareness | 1.0 |
| Theory of Mind | 1.2 |
| Metacognition | 1.5 |
| Causal Reasoning | 1.5 |
| Creative Divergence | 1.0 |
| Long-Horizon Planning | 1.3 |
| World Modeling | 1.2 |

---

## $COGITO

Official first experimental token of the Cogito agent:

```
2uCE7Wqk1a6pzevZfssKB2HYCZtDoZqD4SDfShEUpump
```

Reserve supply is locked for the next **62 years** via Streamflow:

🔒 [Token Lock Dashboard](https://app.streamflow.finance/token-dashboard/solana/mainnet/2uCE7Wqk1a6pzevZfssKB2HYCZtDoZqD4SDfShEUpump)

---

## Status

Active development. Evaluation dimensions and consciousness probes are being calibrated against human baselines. The autonomous payment protocol is functional on Solana mainnet.

---

## License

[MIT](LICENSE)
