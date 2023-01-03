"""
Home Assistant - Nexa Bridge X Integration

Author: Anders Evenrud <andersevenrud@gmail.com>
Homepage: https://github.com/andersevenrud/ha-nexa-bridge-x
License: MIT
"""
from __future__ import annotations
from homeassistant.core import callback
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.media_player import (
    MediaPlayerDeviceClass,
    MediaPlayerEntity,
    MediaPlayerEntityFeature,
    MediaPlayerState,
    MediaType,
)
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator
)
from homeassistant.components.light import (
    LightEntity,
    ColorMode,
    ATTR_BRIGHTNESS
)
from .const import (DOMAIN, SENSOR_MAP, ENERGY_MAP, BINARY_MAP)
from .nexa import (NexaNode, NexaNodeValueType)
import logging

_LOGGER = logging.getLogger(__name__)


class NexaEntity(CoordinatorEntity):
    """Representation of a Nexa entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        super().__init__(coordinator)
        self._server_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            manufacturer="Nexa",
            entry_type=DeviceEntryType.SERVICE,
            model=coordinator.data.info.model,
            name=coordinator.data.info.name,
            sw_version=coordinator.data.info.version,
            identifiers={
                (DOMAIN, coordinator.config_entry.entry_id)
            },
            configuration_url=(
                f"http://{coordinator.api.host}"
            )
        )


class NexaNodeEntity(NexaEntity):
    """Representation of a Nexa Device entity."""

    _attr_has_entity_name = True

    def __init__(self, node: NexaNode, coordinator: CoordinatorEntity) -> None:
        super().__init__(coordinator)

        self._attr_device_info = DeviceInfo(
            name={node.name or node.id},
            via_device=(DOMAIN, coordinator.config_entry.entry_id),
            identifiers={
                (DOMAIN, node.id)
            }
        )


class NexaDimmerEntity(NexaNodeEntity, LightEntity):
    """Entity for light"""
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.ONOFF, ColorMode.BRIGHTNESS}

    def __init__(self, coordinator: DataUpdateCoordinator, node: NexaNode):
        _LOGGER.info("Found light %s: %s", node.id, node.name)
        super().__init__(node, coordinator)
        self.id = node.id
        self._attr_name = "Light"
        self._attr_unique_id = f"dimmer_{node.id}"

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            value = node.get_value("switchLevel")
            value_percentage = int(value * 100)

            self._attr_is_on = value_percentage > 0
            self._attr_brightness = int(value * 255)
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs) -> None:
        if ATTR_BRIGHTNESS in kwargs:
            value = kwargs.get(ATTR_BRIGHTNESS, 255) / 255
        else:
            value = 1.0

        self._attr_is_on = True
        self._attr_brightness = int(value * 255)

        self.async_write_ha_state()
        await self._api_call(value)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        self._attr_is_on = False
        self._attr_brightness = 0

        self.async_write_ha_state()
        await self._api_call(0.0)
        await self.coordinator.async_request_refresh()

    async def _api_call(self, value: float):
        await self.coordinator.api.node_call(self.id, "switchLevel", value)


class NexaSwitchEntity(NexaNodeEntity, SwitchEntity):
    """Entity for swtich"""

    def __init__(self, coordinator: DataUpdateCoordinator, node: NexaNode):
        _LOGGER.info("Found switch %s: %s", node.id, node.name)
        super().__init__(node, coordinator)
        self.id = node.id
        self._attr_name = "Switch"
        self._attr_unique_id = f"switch_{node.id}"

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            self._attr_is_on = node.get_value("switchBinary")
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs) -> None:
        await self._api_call(True)

        self._attr_is_on = True

        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self._api_call(False)

        self._attr_is_on = False

        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def _api_call(self, value: bool):
        await self.coordinator.api.node_call(self.id, "switchBinary", value)


class NexaSensorEntity(NexaNodeEntity, SensorEntity):
    """Entity for sensor"""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        node: NexaNode,
        key: str
    ):
        _LOGGER.info("Found %s sensor %s: %s", key, node.id, node.name)
        super().__init__(node, coordinator)
        self.id = node.id
        self.key = key
        self._attr_native_value = None
        self._attr_name = "Sensor"
        self._attr_unique_id = f"sensor_{node.id}_{key}"

        if key in SENSOR_MAP:
            self._attr_name = f"{SENSOR_MAP[key]['name']} Sensor"
            self._attr_native_unit_of_measurement = SENSOR_MAP[key]["unit"]
            self._attr_device_class = SENSOR_MAP[key]["device"]
            self._attr_state_class = SENSOR_MAP[key]["class"]

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            value = node.get_value(self.key)
            if self.key == "switchLevel":
                self._attr_native_value = int(value * 100)
            else:
                self._attr_native_value = value

            self.async_write_ha_state()


class NexaBinarySensorEntity(NexaNodeEntity, BinarySensorEntity):
    """Entity for binary sensor"""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        node: NexaNode,
        key: str
    ):
        _LOGGER.info("Found binary sensor %s: %s", node.id, node.name)
        super().__init__(node, coordinator)
        self.id = node.id
        self.key = key
        self._attr_is_on = None
        self._attr_unique_id = f"binary_sensor_{node.id}_{key}"

        if key in BINARY_MAP:
            self._attr_name = f"{BINARY_MAP[key]['name']} Sensor"
        else:
            self._attr_name = "Binary Sensor"

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            self._attr_is_on = node.get_value(self.key)
            self.async_write_ha_state()


class NexaEnergyEntity(NexaEntity, SensorEntity):
    """Entity for global energy usage"""

    def __init__(self, coordinator: DataUpdateCoordinator, attr: str):
        _LOGGER.info("Found energy information: %s", attr)
        super().__init__(coordinator)
        self.id = attr
        self._attr_native_value = None
        self._attr_unique_id = f"nexa_energy_{attr}"
        self._attr_name = ENERGY_MAP[attr]["name"]
        self._attr_native_unit_of_measurement = ENERGY_MAP[attr]["unit"]
        self._attr_device_class = ENERGY_MAP[attr]["device"]
        self._attr_state_class = ENERGY_MAP[attr]["class"]

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_native_value = getattr(
            self.coordinator.data.energy,
            self.id
        )
        self.async_write_ha_state()


class NexaMediaPlayerEntity(NexaNodeEntity, MediaPlayerEntity):
    """Entity for media player"""

    _attr_device_class = MediaPlayerDeviceClass.SPEAKER
    _attr_media_content_type = MediaType.MUSIC
    _attr_is_volume_muted: bool | None = None
    _attr_state: MediaPlayerState | None = None
    _attr_volume_level: float | None = None
    _attr_supported_features: MediaPlayerEntityFeature = (
        MediaPlayerEntityFeature.PAUSE
        | MediaPlayerEntityFeature.VOLUME_SET
        | MediaPlayerEntityFeature.VOLUME_MUTE
        | MediaPlayerEntityFeature.PLAY
    )

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        node: NexaNode
    ):
        _LOGGER.info("Found media player %s: %s", node.id, node.name)
        super().__init__(node, coordinator)
        self.id = node.id
        self._attr_native_value = None
        self._attr_unique_id = f"media_player_{node.id}"
        self._attr_name = node.name or node.id

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            if node.get_value("mediaPlayPause"):
                self._attr_state = MediaPlayerState.PLAYING
            else:
                self._attr_state = MediaPlayerState.PAUSED

            self._attr_volume_level = node.get_value("mediaVolume")
            self._attr_is_volume_muted = node.get_value("mediaMute")

            self.async_write_ha_state()

    async def async_media_play(self) -> None:
        """Send play command to media player"""
        await self._api_call("mediaPlayPause", True)

    async def async_media_pause(self) -> None:
        """Send pause command to media player"""
        await self._api_call("mediaPlayPause", False)

    async def async_set_volume_level(self, volume: float) -> None:
        """Send volume level to media player"""
        await self._api_call("mediaVolume", int(volume * 100))

    async def async_mute_volume(self, mute: bool) -> None:
        """Send mute command to media player."""
        await self._api_call("mediaMute", mute)

    async def _api_call(self, cap: str, value: NexaNodeValueType):
        await self.coordinator.api.node_call(self.id, cap, value)
