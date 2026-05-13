from __future__ import annotations

from pathlib import Path

from src.core.config_service import ConfigService
from src.engine.services.images_service import ImagesService
from src.engine.services.sounds_service import SoundsService
from src.engine.services.texts_service import TextsService


class ServiceLocator:
    config: ConfigService
    images_service: ImagesService
    sounds_service: SoundsService
    texts_service: TextsService

    @classmethod
    def bootstrap(cls, root_path: Path) -> None:
        cls.config = ConfigService(root_path)
        cls.images_service = ImagesService(root_path)
        cls.sounds_service = SoundsService(root_path)
        cls.texts_service = TextsService(root_path)
