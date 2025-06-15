"""
Home Assistant - Nexa Bridge X Integration

Author: Anders Evenrud <andersevenrud@gmail.com>
Homepage: https://github.com/andersevenrud/ha-nexa-bridge-x
License: MIT
"""
from __future__ import annotations
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .entities import NexaMotorButtonEntity

COMMANDS = (
    {"command": "up", "label": "Up", "icon": "mdi:arrow-up"},
    {"command": "down", "label": "Down", "icon": "mdi:arrow-down"},
    {"command": "stop", "label": "Stop", "icon": "mdi:stop-circle"},
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all detected buttons"""
    coordinator = hass.data[DOMAIN][entry.entry_id].coordinator
    entities = (
        NexaMotorButtonEntity(
            coordinator,
            node,
            cmd["label"],
            cmd["command"],
            cmd["icon"]
        )
        for cmd in COMMANDS
        for node in coordinator.data.nodes
        if node.is_motor()
    )

    if entities:
        async_add_entities(entities)
