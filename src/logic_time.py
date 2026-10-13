from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter
from typing import Dict, Optional


def get_utc_now() -> datetime:
    """Devuelve la fecha actual en UTC."""
    return datetime.now(timezone.utc)


def iso_now() -> str:
    """Devuelve la fecha actual en formato ISO 8601."""
    return get_utc_now().isoformat()


def elapsed_seconds(start_time: float) -> float:
    """Calcula el tiempo transcurrido desde un punto inicial usando perf_counter."""
    return perf_counter() - start_time


def format_elapsed(seconds: float) -> str:
    """Formatea segundos en una cadena legible."""
    minutes, seconds = divmod(float(seconds), 60)
    hours, minutes = divmod(minutes, 60)

    parts = []
    if hours:
        parts.append(f"{int(hours)}h")
    if minutes or hours:
        parts.append(f"{int(minutes)}m")
    parts.append(f"{seconds:.2f}s")
    return " ".join(parts)


def time_window(start: datetime, end: Optional[datetime] = None) -> Dict[str, str]:
    """Devuelve un diccionario con los límites del intervalo temporal."""
    if end is None:
        end = get_utc_now()

    return {
        "start": start.isoformat(),
        "end": end.isoformat(),
    }
