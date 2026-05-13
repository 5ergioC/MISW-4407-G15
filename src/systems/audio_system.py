from src.components.audio_event import AudioEvent
from src.core.service_locator import ServiceLocator


class AudioSystem:
    def update(self, world, dt: float) -> None:
        del dt
        to_remove: list[tuple[int, AudioEvent]] = []
        for entity, (audio_event,) in world.get_components(AudioEvent):
            ServiceLocator.audio.play(audio_event.sound_path)
            to_remove.append((entity, audio_event))
        for entity, audio_event in to_remove:
            world.remove_component(entity, AudioEvent)
