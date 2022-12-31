"""
Home Assistant - Nexa Bridge X Integration

Author: Anders Evenrud <andersevenrud@gmail.com>
Homepage: https://github.com/andersevenrud/ha-nexa-bridge-x
License: MIT
"""
from __future__ import annotations
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from .nexa import NexaPlatform
from .const import DOMAIN
import logging

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.LIGHT,
    Platform.BINARY_SENSOR,
    Platform.MEDIA_PLAYER
]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HA integration entry"""
    hass.data.setdefault(DOMAIN, {})

    platform = NexaPlatform(hass, entry)
    hass.data[DOMAIN][entry.entry_id] = platform

    await platform.init()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload HA integration entry"""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS
    ):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
