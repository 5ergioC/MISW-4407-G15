from dataclasses import dataclass, field


@dataclass
class Particle:
    kind: str = "generic"
    start_color: tuple[int, int, int] = field(default_factory=lambda: (255, 255, 255))
    end_color: tuple[int, int, int] = field(default_factory=lambda: (255, 0, 0))
    lifetime_max: float = 0.6
