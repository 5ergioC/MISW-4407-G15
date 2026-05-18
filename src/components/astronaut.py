from dataclasses import dataclass


@dataclass
class Astronaut:
    state: str = "idle"
    carrier_entity: int | None = None
    fall_start_y: float | None = None
    rescued_from_fall: bool = False
    deposited: bool = False
