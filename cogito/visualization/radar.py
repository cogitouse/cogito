"""Radar chart visualization for consciousness maps and Cogito Scores."""

from __future__ import annotations

import math
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def generate_radar_chart(
    labels: list[str],
    values: list[float],
    title: str = "Consciousness Map",
    output_path: str | Path = "reports/consciousness_map.svg",
) -> Path:
    """Generate an SVG radar chart."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        logger.error("matplotlib required for visualization")
        raise

    n = len(labels)
    angles = [i / n * 2 * math.pi for i in range(n)]
    angles += angles[:1]
    values_plot = values + values[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.fill(angles, values_plot, alpha=0.25, color="#76b900")
    ax.plot(angles, values_plot, color="#76b900", linewidth=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, size=9)
    ax.set_ylim(0, 1.0)
    ax.set_title(title, size=14, weight="bold", pad=20)
    ax.grid(True, alpha=0.3)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, format="svg", bbox_inches="tight", transparent=True)
    plt.close(fig)

    logger.info("radar chart saved to %s", out)
    return out


def generate_dimension_chart(
    dimension_scores: dict[str, float],
    title: str = "Cogito Score Breakdown",
    output_path: str | Path = "reports/cogito_dimensions.svg",
) -> Path:
    """Generate a radar chart from Cogito evaluation dimension scores."""
    labels = [k.replace("_", " ").title() for k in dimension_scores.keys()]
    values = [v / 100.0 for v in dimension_scores.values()]  # normalize to 0-1
    return generate_radar_chart(labels, values, title=title, output_path=output_path)
