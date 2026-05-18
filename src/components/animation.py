from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Animation:
    frames: list[str] = field(default_factory=list)
    frame_index: int = 0
    frame_time: float = 0.1
    elapsed: float = 0.0
    loop: bool = True
    frame_count: int = 0

