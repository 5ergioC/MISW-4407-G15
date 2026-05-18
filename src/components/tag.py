from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Tag:
    labels: set[str] = field(default_factory=set)

    def __init__(self, *labels: str) -> None:
        self.labels = {label for label in labels if label}

    def has(self, label: str) -> bool:
        return label in self.labels
