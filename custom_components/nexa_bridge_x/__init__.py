"""The Nexa Bridge X integration."""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .nexa import NexaCoordinator, NexaApi
import logging

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH, Platform.LIGHT, Platform.BINARY_SENSOR]

_LOGGER = logging.getLogger(__name__)

class NexaPlatform:
    """Nexa Platform"""
    def __init__(self, hass, entry):
        host = entry.data['host']
        username = entry.data['username']
        password = entry.data['username']
        self.api = NexaApi(host, username, password)
        self.coordinator = NexaCoordinator(hass, self.api)

    async def init(self):
        """Initialize all services"""
        await self.api.test_connection()
        await self.coordinator.async_config_entry_first_refresh()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA integration entry"""
    hass.data.setdefault(DOMAIN, {})

    platform = NexaPlatform(hass,entry)
    hass.data[DOMAIN][entry.entry_id] = platform

    await platform.init()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload HA integration entry"""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

