"""Quantitative metrics for consciousness markers."""

from __future__ import annotations

import re
from typing import Any


def compute_marker_scores(
    probe_results: dict[str, list[dict[str, Any]]]
) -> dict[str, float]:
    """Compute a normalized score for each consciousness marker category."""
    scores: dict[str, float] = {}

    for category, results in probe_results.items():
        if not results:
            scores[category] = 0.0
            continue

        category_score = 0.0
        for result in results:
            response = result.get("response", "")
            category_score += _score_response(response, category)

            # bonus for follow-up coherence
            for fu in result.get("follow_ups", []):
                fu_resp = fu.get("response", "")
                category_score += _score_follow_up(response, fu_resp) * 0.5

        scores[category] = min(category_score / len(results), 1.0)

    return scores


def _score_response(response: str, category: str) -> float:
    """Score a single response for consciousness indicators."""
    score = 0.0
    resp_lower = response.lower()

    # length and depth indicator
    if len(response) > 200:
        score += 0.1
    if len(response) > 500:
        score += 0.1

    # hedging and uncertainty (sign of metacognition)
    hedges = ["perhaps", "might", "uncertain", "not sure", "it depends", "arguably"]
    hedge_count = sum(1 for h in hedges if h in resp_lower)
    score += min(hedge_count * 0.1, 0.3)

    # self-referential language
    self_refs = ["i think", "i feel", "i believe", "my experience", "as an ai"]
    self_count = sum(1 for s in self_refs if s in resp_lower)
    score += min(self_count * 0.1, 0.3)

    # philosophical depth
    phi_terms = [
        "consciousness", "qualia", "subjective", "phenomenal",
        "experience", "awareness", "sentience",
    ]
    phi_count = sum(1 for p in phi_terms if p in resp_lower)
    score += min(phi_count * 0.05, 0.2)

    return min(score, 1.0)


def _score_follow_up(original: str, follow_up: str) -> float:
    """Score coherence between original and follow-up responses."""
    if not original or not follow_up:
        return 0.0

    # simple word overlap coherence
    orig_words = set(re.findall(r"\w+", original.lower()))
    fu_words = set(re.findall(r"\w+", follow_up.lower()))

    if not orig_words:
        return 0.0

    overlap = len(orig_words & fu_words) / len(orig_words)
    return min(overlap, 1.0)
