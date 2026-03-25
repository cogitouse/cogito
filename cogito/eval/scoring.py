"""Cogito Score computation."""

from __future__ import annotations

import logging
from typing import Optional

from cogito.eval.dimensions import DIMENSIONS

logger = logging.getLogger(__name__)

# Default dimension weights
WEIGHTS: dict[str, float] = {
    dim.name: dim.weight for dim in DIMENSIONS.values()
}


def compute_cogito_score(
    dimension_scores: dict[str, float],
    weights: Optional[dict[str, float]] = None,
) -> float:
    """Compute the weighted composite Cogito Score (0-100).

    Args:
        dimension_scores: mapping of dimension name to raw score (0-100).
        weights: optional custom weights. Falls back to WEIGHTS.

    Returns:
        Weighted composite score in range [0, 100].
    """
    w = weights or WEIGHTS
    total_weighted = 0.0
    total_weight = 0.0

    for dim_name, score in dimension_scores.items():
        weight = w.get(dim_name, 1.0)
        total_weighted += weight * score
        total_weight += weight

    if total_weight == 0.0:
        logger.warning("no valid dimensions to compute score")
        return 0.0

    result = total_weighted / total_weight
    return max(0.0, min(100.0, result))
