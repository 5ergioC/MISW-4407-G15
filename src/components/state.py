from dataclasses import dataclass


@dataclass
class State:
    name: str
    elapsed: float = 0.0

