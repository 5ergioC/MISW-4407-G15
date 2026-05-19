from __future__ import annotations

from typing import Callable

import pygame

from src.components.input_command import CommandPhase, InputCommand

_AXIS_DEAD_ZONE = 0.25

# Button mappings (standard Xbox/PS layout)
_BTN_FIRE        = 0   # A / Cross
_BTN_SMART_BOMB  = 1   # B / Circle
_BTN_PAUSE       = 7   # Start
_BTN_MENU        = 6   # Select / Back

_AXIS_H = 0  # left stick horizontal
_AXIS_V = 1  # left stick vertical


class GamepadSystem:
    def __init__(self) -> None:
        self._joystick: pygame.joystick.JoystickType | None = None
        self._prev_buttons: dict[int, bool] = {}
        self._prev_dirs: dict[str, bool] = {
            "left": False, "right": False, "up": False, "down": False,
        }
        self._refresh_joystick()

    def _refresh_joystick(self) -> None:
        count = pygame.joystick.get_count()
        if count > 0:
            joy = pygame.joystick.Joystick(0)
            joy.init()
            self._joystick = joy
        else:
            self._joystick = None

    def update(self, world, do_action: Callable) -> None:
        if self._joystick is None:
            self._refresh_joystick()
            return

        joy = self._joystick

        # ── Axes → directional commands ────────────────────────────────
        try:
            ax = joy.get_axis(_AXIS_H)
            ay = joy.get_axis(_AXIS_V)
        except Exception:
            return

        dirs = {
            "left":  ax < -_AXIS_DEAD_ZONE,
            "right": ax >  _AXIS_DEAD_ZONE,
            "up":    ay < -_AXIS_DEAD_ZONE,
            "down":  ay >  _AXIS_DEAD_ZONE,
        }
        name_map = {
            "left":  "PLAYER_LEFT",
            "right": "PLAYER_RIGHT",
            "up":    "PLAYER_UP",
            "down":  "PLAYER_DOWN",
        }
        for key, active in dirs.items():
            prev = self._prev_dirs[key]
            if active != prev:
                phase = CommandPhase.START if active else CommandPhase.END
                do_action(InputCommand(name=name_map[key], key=-1, phase=phase, active=active))
            elif active:
                # Keep sending START so thrust_input stays set
                do_action(InputCommand(name=name_map[key], key=-1, phase=CommandPhase.START, active=True))
        self._prev_dirs = dirs

        # ── Buttons ─────────────────────────────────────────────────────
        btn_map = {
            _BTN_FIRE:       "PLAYER_FIRE",
            _BTN_SMART_BOMB: "PLAYER_SMART_BOMB",
            _BTN_PAUSE:      "PLAYER_PAUSE",
            _BTN_MENU:       "PLAYER_MENU",
        }
        for btn_idx, cmd_name in btn_map.items():
            try:
                pressed = bool(joy.get_button(btn_idx))
            except Exception:
                continue
            prev = self._prev_buttons.get(btn_idx, False)
            if pressed and not prev:
                do_action(InputCommand(name=cmd_name, key=-1, phase=CommandPhase.START, active=True))
            elif not pressed and prev:
                do_action(InputCommand(name=cmd_name, key=-1, phase=CommandPhase.END, active=False))
            self._prev_buttons[btn_idx] = pressed

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type in (pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED):
            self._refresh_joystick()
