from __future__ import annotations
from homeassistant.core import callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.components.light import (
    LightEntity,
    ColorMode,
    ATTR_BRIGHTNESS
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.const import (
    ELECTRIC_POTENTIAL_VOLT,
    POWER_WATT,
    ELECTRIC_CURRENT_AMPERE,
    ENERGY_KILO_WATT_HOUR,
    PERCENTAGE
)
import logging

SENSOR_MAP = {
    'switchLevel': {
        'name': 'Level',
        'unit': PERCENTAGE,
        'device': None
    },
    'meter': {
        'name': 'Energy',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
    'power': {
        'name': 'Wattage',
        'unit': POWER_WATT,
        'device': SensorDeviceClass.POWER
    },
    'electric_voltage': {
        'name': 'Voltage',
        'unit': ELECTRIC_POTENTIAL_VOLT,
        'device': SensorDeviceClass.VOLTAGE
    },
    'electric_ampere': {
        'name': 'Amperage',
        'unit': ELECTRIC_CURRENT_AMPERE,
        'device': SensorDeviceClass.CURRENT
    }
}

ENERGY_MAP = {
    'totalKilowattHours': {
        'name': 'NEXA Total kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
    'currentWattage': {
        'name': 'NEXA Current W',
        'unit': POWER_WATT,
        'device': SensorDeviceClass.POWER
    },
    'currentKilowattHours': {
        'name': 'NEXA Current kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
    'todayKilowattHours': {
        'name': 'NEXA Today kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
    'yesterdayKilowattHours': {
        'name': 'NEXA Yesterday kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
    'monthKilowattHours': {
        'name': 'NEXA Month kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
}

_LOGGER = logging.getLogger(__name__)

def create_friendly_name(prefix, node):
    return f"{prefix} {node.name or node.id}"

class NexaDimmerEntity(CoordinatorEntity, LightEntity):
    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.ONOFF, ColorMode.BRIGHTNESS}

    def __init__(self, coordinator, node):
        super().__init__(coordinator)
        self.id = node.id
        self.switch_to_state = None
        self._attr_name = create_friendly_name("Light", node)
        self._attr_unique_id = f"dimmer_{node.id}"

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            v = node.get_value('switchLevel')
            vv = int(v * 100)

            if self.switch_to_state is not None:
                self._attr_is_on = self.switch_to_state
                if self.switch_to_state == True and vv == 0:
                    self.switch_to_state = None
                if self.switch_to_state == False and vv > 0:
                    self.switch_to_state = None
            else:
                self._attr_is_on = vv > 0

            self._attr_brightness = int(v * 255)
            self._attr_name = create_friendly_name("Light", node)
            self.async_write_ha_state()
        else:
            self.switch_to_state = False

    async def async_turn_on(self, **kwargs):
        if ATTR_BRIGHTNESS in kwargs:
            v = kwargs.get(ATTR_BRIGHTNESS, 255)
            await self.coordinator.handle_dimmer(self.id, v / 255)
        else:
            v = 1.0
            await self.coordinator.handle_dimmer(self.id, 1)

        self.switch_to_state = True
        self._attr_is_on = True
        self._attr_brightness = v

        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        self.switch_to_state = False
        self._attr_is_on = False
        self._attr_brightness = 0

        self.async_write_ha_state()
        await self.coordinator.handle_dimmer(self.id, 0)
        await self.coordinator.async_request_refresh()


class NexaSwitchEntity(CoordinatorEntity, SwitchEntity):
    def __init__(self, coordinator, node, is_binary = True):
        super().__init__(coordinator)
        self.id = node.id
        self.is_binary = is_binary
        self._attr_name = create_friendly_name("Switch", node)
        self._attr_unique_id = f"switch_{node.id}"

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            self._attr_is_on = node.get_value('switchBinary')
            self._attr_name = create_friendly_name("Switch", node)
            self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        if self.is_binary:
            await self.coordinator.handle_switch(self.id, True)
        else:
            await self.coordinator.handle_dimmer(self.id, 1)

        self._attr_is_on = True

        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs):
        if self.is_binary:
            await self.coordinator.handle_switch(self.id, False)
        else:
            await self.coordinator.handle_dimmer(self.id, 0)

        self._attr_is_on = False

        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()


class NexaSensorEntity(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, node, key):
        super().__init__(coordinator)
        self.id = node.id
        self.key = key
        self._attr_native_value = None
        self._attr_name = create_friendly_name("Sensor", node)
        self._attr_unique_id = f"sensor_{node.id}_{str.lower(key)}"

        self._attr_native_value_class = SensorStateClass.MEASUREMENT
        if key in SENSOR_MAP:
            self._attr_name = create_friendly_name(f"{SENSOR_MAP[key]['name']} Sensor", node)
            self._attr_native_unit_of_measurement = SENSOR_MAP[key]['unit']
            self._attr_device_class = SENSOR_MAP[key]['device']

    @callback
    def _handle_coordinator_update(self) -> None:
        node = self.coordinator.get_node_by_id(self.id)
        if node:
            self._attr_native_value = node.get_value(self.key)
            if self.key in SENSOR_MAP:
                self._attr_name = create_friendly_name(f"{SENSOR_MAP[self.key]['name']} Sensor", node)
            else:
                self._attr_name = create_friendly_name("Sensor", node)
            self.async_write_ha_state()


class NexaBinarySensorEntity(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, node, key):
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


class NexaEnergyEntity(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, id):
        super().__init__(coordinator)
        self.id = id
        self._attr_native_value = None
        self._attr_unique_id = f"nexa_energy_{id}"
        self._attr_name = ENERGY_MAP[id]['name']
        self._attr_native_unit_of_measurement = ENERGY_MAP[id]['unit']
        self._attr_device_class = ENERGY_MAP[id]['device']

        if id == "totalKilowattHours":
            self._attr_native_value_class = SensorStateClass.TOTAL_INCREASING

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_native_value = getattr(self.coordinator.data.energy, self.id)
        self.async_write_ha_state()
