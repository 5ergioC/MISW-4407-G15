from __future__ import annotations

import uuid
from collections.abc import Iterable

import esper


class ECSWorld:
    def __init__(self, name: str | None = None) -> None:
        self.name = name or f"world-{uuid.uuid4()}"
        esper.switch_world(self.name)

    def _activate(self) -> None:
        esper.switch_world(self.name)

    def create_entity(self, *components) -> int:
        self._activate()
        return esper.create_entity(*components)

    def add_component(self, entity: int, component, type_alias=None) -> None:
        self._activate()
        esper.add_component(entity, component, type_alias)

    def remove_component(self, entity: int, component_type):
        self._activate()
        return esper.remove_component(entity, component_type)

    def has_component(self, entity: int, component_type) -> bool:
        self._activate()
        try:
            return esper.has_component(entity, component_type)
        except (KeyError, ValueError):
            return False

    def component_for_entity(self, entity: int, component_type):
        self._activate()
        try:
            return esper.component_for_entity(entity, component_type)
        except (KeyError, ValueError):
            return None

    def get_components(self, *component_types) -> Iterable[tuple[int, tuple]]:
        self._activate()
        return list(esper.get_components(*component_types))

    def delete_entity(self, entity: int, immediate: bool = False) -> None:
        self._activate()
        try:
            esper.delete_entity(entity, immediate=immediate)
        except (KeyError, ValueError):
            pass

    def entity_exists(self, entity: int) -> bool:
        self._activate()
        return esper.entity_exists(entity)

    def clear_database(self) -> None:
        self._activate()
        esper.clear_database()
