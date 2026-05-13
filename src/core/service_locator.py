from __future__ import annotations

from pathlib import Path

from src.core.asset_service import AssetService
from src.core.audio_service import AudioService
from src.core.config_service import ConfigService


class ServiceLocator:
    config: ConfigService
    assets: AssetService
    audio: AudioService

    @classmethod
    def bootstrap(cls, root_path: Path) -> None:
        cls.config = ConfigService(root_path)
        cls.assets = AssetService(root_path)
        cls.audio = AudioService(root_path)
