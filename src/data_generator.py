from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

import numpy as np
import pandas as pd


@dataclass
class DataGeneratorConfig:
    rows: int = 200
    seed: int = 42
    feature_count: int = 5
    noise: float = 0.15


def generate_synthetic_dataset(
    rows: int = 200,
    seed: int = 42,
    feature_count: int = 5,
    noise: float = 0.15,
    target_name: str = "target",
    include_id: bool = True,
) -> pd.DataFrame:
    """Genera un dataset sintético con variables numéricas y una columna objetivo."""
    rng = np.random.default_rng(seed)

    features = rng.normal(0, 1, size=(rows, feature_count))
    weights = np.linspace(1, 3, feature_count)
    linear_signal = features @ weights
    target = (linear_signal + rng.normal(0, noise, size=rows)) > 0

    data = {f"feature_{index}": features[:, index] for index in range(feature_count)}
    data[target_name] = target.astype(int)

    if include_id:
        data["id"] = np.arange(1, rows + 1)

    return pd.DataFrame(data)


def generate_batch_datasets(
    batch_sizes: Iterable[int] | None = None,
    seed: int = 42,
    feature_count: int = 5,
) -> List[pd.DataFrame]:
    """Genera varios datasets sintéticos en una sola ejecución."""
    if batch_sizes is None:
        batch_sizes = [50, 100, 200]

    datasets: List[pd.DataFrame] = []
    for index, rows in enumerate(batch_sizes):
        current_seed = seed + index
        datasets.append(
            generate_synthetic_dataset(
                rows=rows,
                seed=current_seed,
                feature_count=feature_count,
            )
        )
    return datasets
