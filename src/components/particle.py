from dataclasses import dataclass


@dataclass
class Particle:
    # TODO(P4): Add color, fade, and explosion metadata when particle effects are implemented.
    kind: str = "generic"
