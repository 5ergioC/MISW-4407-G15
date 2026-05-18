from dataclasses import dataclass


@dataclass
class Enemy:
    kind: str
    state: str = "idle"
    target_entity: int | None = None
    carried_entity: int | None = None
    alerting: bool = False
