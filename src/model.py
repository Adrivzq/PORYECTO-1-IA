from typing import Dict, Tuple

import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


def train_baseline_model(
    features: pd.DataFrame,
    target: pd.Series,
    model: BaseEstimator,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[BaseEstimator, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """Entrena un modelo base con división train/test."""
    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target if target.nunique() > 1 else None,
    )

    model.fit(X_train, y_train)
    return model, X_train, y_train, X_test, y_test


def evaluate_model(model: BaseEstimator, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
    """Evalúa el modelo con métricas básicas de clasificación."""
    predictions = model.predict(X_test)

    return {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, average="weighted", zero_division=0),
        "recall": recall_score(y_test, predictions, average="weighted", zero_division=0),
        "f1": f1_score(y_test, predictions, average="weighted", zero_division=0),
    }
