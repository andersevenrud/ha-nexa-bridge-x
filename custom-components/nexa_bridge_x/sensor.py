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
    api = hass.data[DOMAIN][entry.entry_id].api
    coordinator = hass.data[DOMAIN][entry.entry_id].coordinator

    entities = [
        NexaEnergyEntity(coordinator, 'totalKilowattHours'),
        NexaEnergyEntity(coordinator, 'currentWattage'),
        NexaEnergyEntity(coordinator, 'todayKilowattHours'),
        NexaEnergyEntity(coordinator, 'currentKilowattHours'),
        NexaEnergyEntity(coordinator, 'yesterdayKilowattHours'),
        NexaEnergyEntity(coordinator, 'monthKilowattHours'),
    ]

    for node in coordinator.data.nodes:
        if node.is_sensor():
            for n in node.get_sensor_capabilities():
                _LOGGER.info(f"Found sensor {node.id}: {node.name} - {n}")
                entities.append(NexaSensorEntity(coordinator, node, n))

    if entities:
        async_add_entities(entities)
