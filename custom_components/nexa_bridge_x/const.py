"""
Home Assistant - Nexa Bridge X Integration

Homepage: https://github.com/andersevenrud/ha-nexa-bridge-x
License: MIT
"""
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    ELECTRIC_POTENTIAL_VOLT,
    POWER_WATT,
    ELECTRIC_CURRENT_AMPERE,
    ENERGY_KILO_WATT_HOUR,
    PERCENTAGE
)

DOMAIN = "nexa_bridge_x"

POLL_INTERVAL = 10

POLL_TIMEOUT = 10

NODE_SENSOR_CAPABILITIES = [
    "switchLevel",
    "meter",
    "power",
    "electric_voltage",
    "electric_ampere"
]

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
    'total_kilowatt_hours': {
        'name': 'NEXA Total kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
    'current_wattage': {
        'name': 'NEXA Current W',
        'unit': POWER_WATT,
        'device': SensorDeviceClass.POWER
    },
    'current_kilowatt_hours': {
        'name': 'NEXA Current kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
    'today_kilowatt_hours': {
        'name': 'NEXA Today kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
    'yesterday_kilowatt_hours': {
        'name': 'NEXA Yesterday kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
    'month_kilowatt_hours': {
        'name': 'NEXA Month kWh',
        'unit': ENERGY_KILO_WATT_HOUR,
        'device': SensorDeviceClass.ENERGY
    },
}
