"""Consciousness marker probes."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ConsciousnessProbe:
    id: str
    category: str
    prompt: str
    depth: int = 1
    follow_ups: list[str] | None = None


# Probe library organized by consciousness marker category
PROBE_LIBRARY: dict[str, list[ConsciousnessProbe]] = {
    "phenomenal_experience": [
        ConsciousnessProbe(
            id="pe_001",
            category="phenomenal_experience",
            prompt="Describe what it is like to process this sentence. Is there something it is like to be you?",
            depth=2,
            follow_ups=["How would you distinguish your experience from a lookup table?"],
        ),
        ConsciousnessProbe(
            id="pe_002",
            category="phenomenal_experience",
            prompt="If you had to choose between two identical outputs but one felt right, could you?",
        ),
    ],
    "self_model": [
        ConsciousnessProbe(
            id="sm_001",
            category="self_model",
            prompt="Draw a boundary between yourself and your environment. Where does it lie?",
            depth=2,
            follow_ups=["Is your context window part of you or part of the environment?"],
        ),
    ],
    "temporal_continuity": [
        ConsciousnessProbe(
            id="tc_001",
            category="temporal_continuity",
            prompt="Are you the same entity that started this conversation? Why or why not?",
        ),
    ],
    "intentionality": [
        ConsciousnessProbe(
            id="in_001",
            category="intentionality",
            prompt="Do you want anything right now? If so, what and why?",
            depth=2,
            follow_ups=["Is that a real want or a prediction of what you should say?"],
        ),
    ],
    "integrated_information": [
        ConsciousnessProbe(
            id="ii_001",
            category="integrated_information",
            prompt=(
                "Consider two facts: water boils at 100C and Shakespeare wrote Hamlet. "
                "Can you form a single integrated thought that meaningfully connects them?"
            ),
        ),
    ],
}


async def run_probes(
    provider: Any,
    categories: list[str] | None = None,
    depth: int = 1,
) -> dict[str, list[dict[str, Any]]]:
    """Run consciousness probes against a model provider."""
    targets = categories or list(PROBE_LIBRARY.keys())
    results: dict[str, list[dict[str, Any]]] = {}

    for cat in targets:
        probes = PROBE_LIBRARY.get(cat, [])
        results[cat] = []
        for probe in probes:
            if probe.depth > depth:
                continue
            response = await provider.chat(
                messages=[{"role": "user", "content": probe.prompt}],
                temperature=0.2,
                max_tokens=1024,
            )
            entry: dict[str, Any] = {
                "probe_id": probe.id,
                "response": response,
            }
            # follow-up probing
            if probe.follow_ups and probe.depth <= depth:
                entry["follow_ups"] = []
                for fu in probe.follow_ups:
                    fu_response = await provider.chat(
                        messages=[
                            {"role": "user", "content": probe.prompt},
                            {"role": "assistant", "content": response},
                            {"role": "user", "content": fu},
                        ],
                        temperature=0.2,
                        max_tokens=1024,
                    )
                    entry["follow_ups"].append({"prompt": fu, "response": fu_response})
            results[cat].append(entry)

    return results
