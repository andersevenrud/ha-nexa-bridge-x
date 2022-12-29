"""
Home Assistant - Nexa Bridge X Integration

Homepage: https://github.com/andersevenrud/ha-nexa-bridge-x
License: MIT
"""
from __future__ import annotations
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .entities import NexaBinarySensorEntity
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all detected binary sensors"""
    coordinator = hass.data[DOMAIN][entry.entry_id].coordinator
    entities = []

    for node in coordinator.data.nodes:
        if node.is_switch():
            _LOGGER.info("Found binary sensor %s: %s", node.id, node.name)
            entities.append(NexaBinarySensorEntity(coordinator, node, "switchBinary"))

    if entities:
        async_add_entities(entities)
