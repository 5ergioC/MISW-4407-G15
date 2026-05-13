from dataclasses import dataclass


@dataclass
class Enemy:
    kind: str
    state: str = "idle"
