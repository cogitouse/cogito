"""Consciousness map generation."""

from __future__ import annotations

import logging
from typing import Any

from cogito.consciousness.metrics import compute_marker_scores

logger = logging.getLogger(__name__)


class ConsciousnessMap:
    """A structured representation of consciousness markers across an AI system."""

    def __init__(self, model_id: str) -> None:
        self.model_id = model_id
        self.markers: dict[str, float] = {}
        self.raw_data: dict[str, list[dict[str, Any]]] = {}

    def build(self, probe_results: dict[str, list[dict[str, Any]]]) -> None:
        """Build the consciousness map from probe results."""
        self.raw_data = probe_results
        self.markers = compute_marker_scores(probe_results)
        logger.info(
            "consciousness map built for %s: %d markers",
            self.model_id,
            len(self.markers),
        )

    def summary(self) -> dict[str, Any]:
        """Return a summary of the consciousness map."""
        if not self.markers:
            return {"model_id": self.model_id, "status": "not_built"}

        avg_score = sum(self.markers.values()) / max(len(self.markers), 1)
        return {
            "model_id": self.model_id,
            "markers": {k: round(v, 3) for k, v in self.markers.items()},
            "mean_score": round(avg_score, 3),
            "strongest": max(self.markers, key=self.markers.get) if self.markers else None,
            "weakest": min(self.markers, key=self.markers.get) if self.markers else None,
        }

    def to_radar_data(self) -> dict[str, list]:
        """Format data for radar chart visualization."""
        labels = list(self.markers.keys())
        values = [self.markers[k] for k in labels]
        return {"labels": labels, "values": values}
