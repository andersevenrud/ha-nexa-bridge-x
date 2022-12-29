from __future__ import annotations
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .entities import NexaDimmerEntity
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all detected lights"""
    coordinator = hass.data[DOMAIN][entry.entry_id].coordinator
    entities = []

    for node in coordinator.data.nodes:
        if node.is_light():
            _LOGGER.info("Found light %s: %s", node.id, node.name)
            entities.append(NexaDimmerEntity(coordinator, node))

    if entities:
        async_add_entities(entities)
