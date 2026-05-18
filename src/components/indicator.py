from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Indicator:
    label: str
    source_entity: int | None = None
    active: bool = True
