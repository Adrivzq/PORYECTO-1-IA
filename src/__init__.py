"""Paquete principal del proyecto de IA."""

from .data_loader import load_csv
from .preprocessing import clean_column_names, normalize_numeric_columns
from .model import train_baseline_model, evaluate_model

__all__ = [
    "load_csv",
    "clean_column_names",
    "normalize_numeric_columns",
    "train_baseline_model",
    "evaluate_model",
]
