from __future__ import annotations


class RewardSystem:
    """Grants +1 life and +1 smart bomb at each 10 000-point milestone."""

    _INTERVAL = 10_000
    _MAX_LIVES = 5
    _MAX_BOMBS = 5

    def update(self, world, shared_state: dict) -> None:
        score = int(shared_state.get("score", 0))
        last = int(shared_state.get("_last_reward_milestone", 0))
        milestone = (score // self._INTERVAL) * self._INTERVAL
        if milestone > 0 and milestone > last:
            shared_state["_last_reward_milestone"] = milestone
            lives = int(shared_state.get("lives", 0))
            bombs = int(shared_state.get("smart_bombs", 0))
            if lives < self._MAX_LIVES:
                shared_state["lives"] = lives + 1
            if bombs < self._MAX_BOMBS:
                shared_state["smart_bombs"] = bombs + 1
            from src.factories.entity_factory import create_audio_event
            create_audio_event(world, "snd/game_start.ogg")
