"""
Home Assistant - Nexa Bridge X Integration

Author: Anders Evenrud <andersevenrud@gmail.com>
Homepage: https://github.com/andersevenrud/ha-nexa-bridge-x
License: MIT
"""
from __future__ import annotations
from itertools import chain
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from .const import (DOMAIN, ENERGY_ATTRS, LEGACY_ENERGY_ATTRS)
from .entities import (
    NexaSensorEntity,
    NexaEnergyEntity
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up all detected sensors"""
    coordinator = hass.data[DOMAIN][entry.entry_id].coordinator

    found_sensors = filter(
        lambda node: node.is_sensor(),
        coordinator.data.nodes
    )

    use_attrs = LEGACY_ENERGY_ATTRS if coordinator.legacy else ENERGY_ATTRS
    energy_entities = (
        NexaEnergyEntity(coordinator, attr)
        for attr in use_attrs
    )

    sensor_entities = (
        NexaSensorEntity(coordinator, node, name)
        for node in found_sensors
        for name in node.get_sensor_capabilities()
    )

    entities = chain(energy_entities, sensor_entities)

    async_add_entities(entities)
