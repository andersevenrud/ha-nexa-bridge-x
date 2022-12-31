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
from .entities import (
    NexaSensorEntity,
    NexaEnergyEntity
)
import logging

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all detected sensors"""
    coordinator = hass.data[DOMAIN][entry.entry_id].coordinator

    entities = [
        NexaEnergyEntity(coordinator, "total_kilowatt_hours"),
        NexaEnergyEntity(coordinator, "current_wattage"),
        NexaEnergyEntity(coordinator, "today_kilowatt_hours"),
        NexaEnergyEntity(coordinator, "current_kilowatt_hours"),
        NexaEnergyEntity(coordinator, "yesterday_kilowatt_hours"),
        NexaEnergyEntity(coordinator, "month_kilowatt_hours"),
    ]

    for node in coordinator.data.nodes:
        if node.is_sensor():
            for name in node.get_sensor_capabilities():
                _LOGGER.info("Found sensor %s: %s - %s",
                             node.id,
                             node.name,
                             name)

                entities.append(NexaSensorEntity(coordinator, node, name))

    if entities:
        async_add_entities(entities)
