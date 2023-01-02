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
from .entities import NexaBinarySensorEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all detected binary sensors"""
    coordinator = hass.data[DOMAIN][entry.entry_id].coordinator

    found_sensors = filter(
        lambda node: node.is_binary_sensor(),
        coordinator.data.nodes
    )

    entities = (
        NexaBinarySensorEntity(coordinator, node, name)
        for node in found_sensors
        for name in node.get_binary_capabilities()
    )

    if entities:
        async_add_entities(entities)
