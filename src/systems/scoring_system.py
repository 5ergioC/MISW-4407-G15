from src.components.score_value import ScoreValue
from src.components.tag import Tag


class ScoringSystem:
    def update(self, world, shared_state: dict[str, object]) -> None:
        total = int(shared_state.get("score", 0))
        consumed: list[int] = []
        for entity, (score_value, tag) in world.get_components(ScoreValue, Tag):
            if not tag.has("score_event"):
                continue
            total += int(score_value.amount)
            consumed.append(entity)
        shared_state["score"] = total
        for entity in consumed:
            world.delete_entity(entity, immediate=True)

