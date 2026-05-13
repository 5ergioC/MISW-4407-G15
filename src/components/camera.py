from dataclasses import dataclass


@dataclass
class CameraTarget:
    look_ahead_x: float = 0.0


@dataclass
class Camera:
    x: float = 0.0
    y: float = 0.0
    width: float = 320.0
    height: float = 256.0
    world_width: float = 640.0
    smoothness: float = 8.0
    look_direction: float = 1.0
    look_ahead_speed_threshold: float = 24.0
