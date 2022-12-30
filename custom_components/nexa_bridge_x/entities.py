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
from .const import (DOMAIN, SENSOR_MAP, ENERGY_MAP)
from .nexa import NexaNode


def create_friendly_name(prefix: str, node: NexaNode) -> str:
    """Create a friendly name for HA"""
    return f"{prefix} {node.name or node.id}"


class NexaEntity(CoordinatorEntity):
    """Representation of a Nexa entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: CoordinatorEntity) -> None:
        super().__init__(coordinator)
        self._server_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            manufacturer="Nexa",
            suggested_area="Indoors",
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


class NexaDimmerEntity(NexaEntity, LightEntity):
    """Entity for light"""
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.ONOFF, ColorMode.BRIGHTNESS}

    def __init__(self, coordinator: DataUpdateCoordinator, node: NexaNode):
        super().__init__(coordinator)
        self.id = node.id
        self.switch_to_state = None
        self._attr_name = create_friendly_name("Light", node)
        self._attr_unique_id = f"dimmer_{node.id}"

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            value = node.get_value('switchLevel')
            value_percentage = int(value * 100)

            if self.switch_to_state is not None:
                self._attr_is_on = self.switch_to_state
                if self.switch_to_state is True and value_percentage == 0:
                    self.switch_to_state = None
                if self.switch_to_state is False and value_percentage > 0:
                    self.switch_to_state = None
            else:
                self._attr_is_on = value_percentage > 0

            self._attr_brightness = int(value * 255)
            self._attr_name = create_friendly_name("Light", node)
            self.async_write_ha_state()
        else:
            self.switch_to_state = False

    async def async_turn_on(self, **kwargs) -> None:
        if ATTR_BRIGHTNESS in kwargs:
            value = kwargs.get(ATTR_BRIGHTNESS, 255)
            await self.coordinator.handle_dimmer(self.id, value / 255)
        else:
            value = 1.0
            await self.coordinator.handle_dimmer(self.id, 1)

        self.switch_to_state = True
        self._attr_is_on = True
        self._attr_brightness = value

        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        self.switch_to_state = False
        self._attr_is_on = False
        self._attr_brightness = 0

        self.async_write_ha_state()
        await self.coordinator.handle_dimmer(self.id, 0)
        await self.coordinator.async_request_refresh()


class NexaSwitchEntity(NexaEntity, SwitchEntity):
    """Entity for swtich"""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        node: NexaNode,
        is_binary: bool = True
    ):
        super().__init__(coordinator)
        self.id = node.id
        self.is_binary = is_binary
        self._attr_name = create_friendly_name("Switch", node)
        self._attr_unique_id = f"switch_{node.id}"

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            if self.is_binary:
                self._attr_is_on = node.get_value('switchBinary')
            else:
                self._attr_is_on = int(node.get_value('switchLevel') * 100) > 0
            self._attr_name = create_friendly_name("Switch", node)
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs) -> None:
        if self.is_binary:
            await self.coordinator.handle_switch(self.id, True)
        else:
            await self.coordinator.handle_dimmer(self.id, 1)

        self._attr_is_on = True

        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        if self.is_binary:
            await self.coordinator.handle_switch(self.id, False)
        else:
            await self.coordinator.handle_dimmer(self.id, 0)

        self._attr_is_on = False

        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()


class NexaSensorEntity(NexaEntity, SensorEntity):
    """Entity for sensor"""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        node: NexaNode,
        key: str
    ):
        super().__init__(coordinator)
        self.id = node.id
        self.key = key
        self._attr_native_value = None
        self._attr_name = create_friendly_name("Sensor", node)
        self._attr_unique_id = f"sensor_{node.id}_{key}"

        if key in SENSOR_MAP:
            friendly = f"{SENSOR_MAP[key]['name']} Sensor"
            self._attr_name = create_friendly_name(friendly, node)
            self._attr_native_unit_of_measurement = SENSOR_MAP[key]['unit']
            self._attr_device_class = SENSOR_MAP[key]['device']
            self._attr_state_class = SENSOR_MAP[key]['class']

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            value = node.get_value(self.key)
            if self.key == 'switchLevel':
                self._attr_native_value = int(value * 100)
            else:
                self._attr_native_value = value

            if self.key in SENSOR_MAP:
                friendly = f"{SENSOR_MAP[self.key]['name']} Sensor"
                self._attr_name = create_friendly_name(friendly, node)
            else:
                self._attr_name = create_friendly_name("Sensor", node)
            self.async_write_ha_state()


class NexaBinarySensorEntity(NexaEntity, BinarySensorEntity):
    """Entity for binary sensor"""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        node: NexaNode,
        key: str
    ):
        super().__init__(coordinator)
        self.id = node.id
        self.key = key
        self._attr_is_on = None
        self._attr_name = create_friendly_name("Binary Sensor", node)
        self._attr_unique_id = f"binary_sensor_{node.id}"

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            self._attr_is_on = node.get_value(self.key)
            self._attr_name = create_friendly_name("Binary Sensor", node)
            self.async_write_ha_state()


class NexaEnergyEntity(NexaEntity, SensorEntity):
    """Entity for global energy usage"""

    def __init__(self, coordinator: DataUpdateCoordinator, attr: str):
        super().__init__(coordinator)
        self.id = attr
        self._attr_native_value = None
        self._attr_unique_id = f"nexa_energy_{attr}"
        self._attr_name = ENERGY_MAP[attr]['name']
        self._attr_native_unit_of_measurement = ENERGY_MAP[attr]['unit']
        self._attr_device_class = ENERGY_MAP[attr]['device']
        self._attr_state_class = ENERGY_MAP[attr]['class']

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_native_value = getattr(
            self.coordinator.data.energy,
            self.id
        )
        self.async_write_ha_state()
