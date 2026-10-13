from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


@dataclass
class OptimizationResult:
    model_name: str
    best_score: float
    metrics: Dict[str, float]


def get_default_models() -> Dict[str, BaseEstimator]:
    """Devuelve una colección básica de modelos para optimizar."""
    return {
        "logistic_regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1000, random_state=42)),
            ]
        ),
        "random_forest": RandomForestClassifier(n_estimators=200, random_state=42),
    }


def optimize_model(
    X: pd.DataFrame,
    y: pd.Series,
    models: Optional[Dict[str, BaseEstimator]] = None,
    cv: int = 5,
    scoring: str = "f1",
) -> OptimizationResult:
    """Evalúa modelos con validación cruzada y devuelve el mejor resultado."""
    if models is None:
        models = get_default_models()

    best_name = ""
    best_score = float("-inf")
    best_metrics: Dict[str, float] = {}

    cv_splitter = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)

    for name, model in models.items():
        scores = cross_val_score(model, X, y, cv=cv_splitter, scoring=scoring)
        score = float(scores.mean())

        if score > best_score:
            best_score = score
            best_name = name

        model.fit(X, y)
        predictions = model.predict(X)
        best_metrics[name] = {
            "mean_cv_score": score,
            "accuracy": accuracy_score(y, predictions),
            "f1": f1_score(y, predictions, average="weighted", zero_division=0),
        }

    return OptimizationResult(
        model_name=best_name,
        best_score=best_score,
        metrics=best_metrics,
    )


def compare_models(
    X: pd.DataFrame,
    y: pd.Series,
    models: Optional[Iterable[BaseEstimator]] = None,
    model_names: Optional[List[str]] = None,
    cv: int = 5,
) -> List[Dict[str, float]]:
    """Compara varios modelos y devuelve un resumen de validación cruzada."""
    model_map = get_default_models() if models is None else dict(zip(model_names or [f"model_{index}" for index in range(len(list(models)))], models))

    results: List[Dict[str, float]] = []
    cv_splitter = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)

    for name, model in model_map.items():
        scores = cross_val_score(model, X, y, cv=cv_splitter, scoring="f1")
        results.append({
            "model": name,
            "mean_f1": float(scores.mean()),
            "std_f1": float(scores.std()),
        })

    return results
