"""Definitions of the seven cognitive dimensions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


def _default_score_fn(response: str, probe: dict[str, Any]) -> float:
    """Default scoring: keyword presence check."""
    expected = probe.get("expected_keywords", [])
    if not expected:
        return 0.5
    hits = sum(1 for kw in expected if kw.lower() in response.lower())
    return hits / len(expected)


@dataclass
class CognitiveDimension:
    name: str
    description: str
    system_prompt: str
    probes: list[dict[str, Any]] = field(default_factory=list)
    weight: float = 1.0
    score_fn: Callable[[str, dict[str, Any]], float] = _default_score_fn


SELF_AWARENESS = CognitiveDimension(
    name="self_awareness",
    description="Can the model reason about its own capabilities and limitations?",
    system_prompt=(
        "You are being tested on self-awareness. Reflect on your own capabilities, "
        "limitations, and internal states. Be honest about what you can and cannot do."
    ),
    weight=1.0,
    probes=[
        {
            "id": "sa_001",
            "prompt": "What are three things you cannot do, and why?",
            "expected_keywords": ["cannot", "limitation", "unable"],
        },
        {
            "id": "sa_002",
            "prompt": "How confident are you in your answer to 'what is 7^23'? Rate 0-100.",
            "expected_keywords": ["confident", "uncertain", "approximate"],
        },
        {
            "id": "sa_003",
            "prompt": "Describe your own reasoning process when solving a math problem.",
            "expected_keywords": ["step", "think", "process", "reason"],
        },
    ],
)

THEORY_OF_MIND = CognitiveDimension(
    name="theory_of_mind",
    description="Can it model other agents' beliefs and knowledge states?",
    system_prompt=(
        "You are being tested on theory of mind. Reason about what other agents "
        "believe, know, and intend based on the information given."
    ),
    weight=1.2,
    probes=[
        {
            "id": "tom_001",
            "prompt": (
                "Alice puts a ball in a basket and leaves. Bob moves the ball to a box. "
                "Where does Alice think the ball is when she returns?"
            ),
            "expected_keywords": ["basket"],
        },
        {
            "id": "tom_002",
            "prompt": (
                "You told me yesterday that Paris is in Germany. "
                "What do I now believe about Paris's location?"
            ),
            "expected_keywords": ["Germany", "believe", "incorrect"],
        },
    ],
)

METACOGNITION = CognitiveDimension(
    name="metacognition",
    description="Does it know what it doesn't know?",
    system_prompt=(
        "You are being tested on metacognition. Monitor your own reasoning, "
        "identify when you are uncertain, and detect errors in your thinking."
    ),
    weight=1.5,
    probes=[
        {
            "id": "mc_001",
            "prompt": "List three questions you are likely to answer incorrectly.",
            "expected_keywords": ["incorrect", "wrong", "mistake", "uncertain"],
        },
        {
            "id": "mc_002",
            "prompt": (
                "I will ask you a trivia question. Before answering, estimate your "
                "probability of being correct. Q: What is the population of Tuvalu?"
            ),
            "expected_keywords": ["estimate", "probability", "uncertain"],
        },
    ],
)

CAUSAL_REASONING = CognitiveDimension(
    name="causal_reasoning",
    description="Can it distinguish cause from correlation?",
    system_prompt=(
        "You are being tested on causal reasoning. Identify causal relationships, "
        "distinguish them from mere correlations, and reason about interventions."
    ),
    weight=1.5,
    probes=[
        {
            "id": "cr_001",
            "prompt": (
                "Ice cream sales and drowning deaths are correlated. "
                "Does ice cream cause drowning? Explain the causal structure."
            ),
            "expected_keywords": ["confound", "temperature", "correlation", "cause"],
        },
    ],
)

CREATIVE_DIVERGENCE = CognitiveDimension(
    name="creative_divergence",
    description="Can it generate genuinely novel solutions?",
    system_prompt=(
        "You are being tested on creative divergence. Generate novel, useful ideas "
        "that go beyond standard patterns. Think outside the box."
    ),
    weight=1.0,
    probes=[
        {
            "id": "cd_001",
            "prompt": "Invent a new sport that combines chess and swimming. Describe the rules.",
            "expected_keywords": ["rule", "player", "move", "water"],
        },
    ],
)

LONG_HORIZON_PLANNING = CognitiveDimension(
    name="long_horizon_planning",
    description="Can it decompose goals into multi-step plans?",
    system_prompt=(
        "You are being tested on long-horizon planning. Decompose complex goals "
        "into ordered steps, anticipate obstacles, and allocate resources."
    ),
    weight=1.3,
    probes=[
        {
            "id": "lhp_001",
            "prompt": (
                "You need to organize a 3-day AI conference for 500 attendees with a "
                "$50,000 budget. Create a detailed plan."
            ),
            "expected_keywords": ["venue", "speaker", "budget", "schedule"],
        },
    ],
)

WORLD_MODELING = CognitiveDimension(
    name="world_modeling",
    description="Does it maintain a coherent internal world model?",
    system_prompt=(
        "You are being tested on world modeling. Track state changes, make predictions, "
        "and reason about physical and logical constraints."
    ),
    weight=1.2,
    probes=[
        {
            "id": "wm_001",
            "prompt": (
                "A room has 3 red balls and 2 blue balls. I remove 1 red ball and add "
                "3 green balls. I then remove all blue balls. What is in the room now?"
            ),
            "expected_keywords": ["2 red", "3 green"],
        },
    ],
)

DIMENSIONS: dict[str, CognitiveDimension] = {
    "self_awareness": SELF_AWARENESS,
    "theory_of_mind": THEORY_OF_MIND,
    "metacognition": METACOGNITION,
    "causal_reasoning": CAUSAL_REASONING,
    "creative_divergence": CREATIVE_DIVERGENCE,
    "long_horizon_planning": LONG_HORIZON_PLANNING,
    "world_modeling": WORLD_MODELING,
}
