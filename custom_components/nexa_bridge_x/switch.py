from __future__ import annotations
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .entities import NexaSwitchEntity
import logging

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    api = hass.data[DOMAIN][entry.entry_id].api
    coordinator = hass.data[DOMAIN][entry.entry_id].coordinator
    entities = []

    for node in coordinator.data.nodes:
        if node.is_switch():
            _LOGGER.info(f"Found switch {node.id}: {node.name}")
            entities.append(NexaSwitchEntity(coordinator, node))
        if node.is_light():
            _LOGGER.info(f"Found simulated switch {node.id}: {node.name}")
            entities.append(NexaSwitchEntity(coordinator, node, False))

    if entities:
        async_add_entities(entities)
