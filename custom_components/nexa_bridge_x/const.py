"""
Home Assistant - Nexa Bridge X Integration

Author: Anders Evenrud <andersevenrud@gmail.com>
Homepage: https://github.com/andersevenrud/ha-nexa-bridge-x
License: MIT
"""
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    ELECTRIC_POTENTIAL_VOLT,
    POWER_WATT,
    ELECTRIC_CURRENT_AMPERE,
    ENERGY_KILO_WATT_HOUR,
    PERCENTAGE,
    TEMP_CELSIUS,
    LIGHT_LUX
)

DOMAIN = "nexa_bridge_x"

POLL_INTERVAL = 10

POLL_TIMEOUT = 10

NODE_BINARY_CAPABILITIES = [
    "notificationContact",
    "notificationMotion",
    "notificationSmoke",
    "notificationWater",
    "notificationTwilight"
]

NODE_SENSOR_CAPABILITIES = [
    "switchLevel",
    "meter",
    "power",
    "electric_voltage",
    "electric_ampere",
    "temperature",
    "humidity",
    "luminance"
]

SENSOR_MAP = {
    'switchLevel': {
        'name': 'Level',
        'unit': PERCENTAGE,
        'device': None,
        'class': SensorStateClass.MEASUREMENT
    },
    'meter': {
        'name': 'Energy',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY,
        'class': SensorStateClass.TOTAL_INCREASING
    },
    'power': {
        'name': 'Wattage',
        'unit': POWER_WATT,
        'device': SensorDeviceClass.POWER,
        'class': SensorStateClass.MEASUREMENT
    },
    'electric_voltage': {
        'name': 'Voltage',
        'unit': ELECTRIC_POTENTIAL_VOLT,
        'device': SensorDeviceClass.VOLTAGE,
        'class': SensorStateClass.MEASUREMENT
    },
    'electric_ampere': {
        'name': 'Amperage',
        'unit': ELECTRIC_CURRENT_AMPERE,
        'device': SensorDeviceClass.CURRENT,
        'class': SensorStateClass.MEASUREMENT
    },
    'temperature': {
        'name': 'Temperature',
        'unit': TEMP_CELSIUS,
        'device': SensorDeviceClass.TEMPERATURE,
        'class': SensorStateClass.MEASUREMENT
    },
    'humidity': {
        'name': 'Temperature',
        'unit': PERCENTAGE,
        'device': SensorDeviceClass.HUMIDITY,
        'class': SensorStateClass.MEASUREMENT
    },
    'luminance': {
        'name': 'Luminance',
        'unit': LIGHT_LUX,
        'device': SensorDeviceClass.ILLUMINANCE,
        'class': SensorStateClass.MEASUREMENT
    },
}

ENERGY_MAP = {
    'total_kilowatt_hours': {
        'name': 'NEXA Total kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY,
        'class': SensorStateClass.TOTAL_INCREASING
    },
    'current_wattage': {
        'name': 'NEXA Current W',
        'unit': POWER_WATT,
        'device': SensorDeviceClass.POWER,
        'class': SensorStateClass.MEASUREMENT
    },
    'current_kilowatt_hours': {
        'name': 'NEXA Current kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY,
        'class': SensorStateClass.MEASUREMENT
    },
    'today_kilowatt_hours': {
        'name': 'NEXA Today kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY,
        'class': SensorStateClass.TOTAL_INCREASING
    },
    'yesterday_kilowatt_hours': {
        'name': 'NEXA Yesterday kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY,
        'class': SensorStateClass.TOTAL_INCREASING
    },
    'month_kilowatt_hours': {
        'name': 'NEXA Month kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY,
        'class': SensorStateClass.TOTAL_INCREASING
    },
}
