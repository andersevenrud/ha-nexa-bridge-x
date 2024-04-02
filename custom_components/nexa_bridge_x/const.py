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
    UnitOfPower,
    UnitOfEnergy,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfTemperature,
    PERCENTAGE,
    LIGHT_LUX
)

DOMAIN = "nexa_bridge_x"

POLL_INTERVAL = 30

POLL_TIMEOUT = 25

CALL_TIMEOUT = 30

RECONNECT_SLEEP = 5

DEFAULT_USERNAME = "nexa"

DEFAULT_PASSWORD = "nexa"

WS_PORT = 8887

HTTP_BASIC_AUTH = False

SWITCH_LEVEL_SENSOR = False

SWITCH_BINARY_SENSOR = False

FORCE_NODE_ENUM = False

NODE_MEDIA_CAPABILITIES = [
    "mediaVolume",
    "mediaPlayPause",
    "mediaMute"
]

NODE_BINARY_CAPABILITIES = [
    "notificationContact",
    "notificationMotion",
    "notificationSmoke",
    "notificationWater",
    "notificationTwilight",
    "notificationTamper",
    "notificationButton",
    "notification"
] + (SWITCH_BINARY_SENSOR and ["switchBinary"] or [])

NODE_SENSOR_CAPABILITIES = [
    "meter",
    "power",
    "electric_voltage",
    "electric_ampere",
    "temperature",
    "humidity",
    "luminance",
    "battery",
    "customEvent"
] + (SWITCH_LEVEL_SENSOR and ["switchLevel"] or [])

ENERGY_ATTRS = [
    "total_kilowatt_hours",
    "current_wattage",
    "current_kilowatt_hours",
    "today_kilowatt_hours",
    "yesterday_kilowatt_hours",
    "month_kilowatt_hours"
]

# TODO: Add support for legacy energy metering
LEGACY_ENERGY_ATTRS = [
    #"total_kilowatt_hours",
    #"current_wattage",
]

BINARY_MAP = {
    "notificationContact": {
        "name": "Contact"
    },
    "notificationMotion": {
        "name": "Motion"
    },
    "notificationSmoke": {
        "name": "Smoke"
    },
    "notificationWater": {
        "name": "Water"
    },
    "notificationTwilight": {
        "name": "Twilight"
    },
    "notificationTamper": {
        "name": "Tamper"
    },
    "notificationButton": {
        "name": "Button"
    },
    "notification": {
        "name": "Value"
    },
    "switchBinary": {
        "name": "Switch"
    },
}

SENSOR_MAP = {
    "switchLevel": {
        "name": "Level",
        "unit": PERCENTAGE,
        "device": None,
        "class": SensorStateClass.MEASUREMENT
    },
    "meter": {
        "name": "Energy",
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.TOTAL_INCREASING
    },
    "power": {
        "name": "Wattage",
        "unit": UnitOfPower.WATT,
        "device": SensorDeviceClass.POWER,
        "class": SensorStateClass.MEASUREMENT
    },
    "electric_voltage": {
        "name": "Voltage",
        "unit": UnitOfElectricPotential.VOLT,
        "device": SensorDeviceClass.VOLTAGE,
        "class": SensorStateClass.MEASUREMENT
    },
    "electric_ampere": {
        "name": "Amperage",
        "unit": UnitOfElectricCurrent.AMPERE,
        "device": SensorDeviceClass.CURRENT,
        "class": SensorStateClass.MEASUREMENT
    },
    "temperature": {
        "name": "Temperature",
        "unit": UnitOfTemperature.CELSIUS,
        "device": SensorDeviceClass.TEMPERATURE,
        "class": SensorStateClass.MEASUREMENT
    },
    "humidity": {
        "name": "Humidity",
        "unit": PERCENTAGE,
        "device": SensorDeviceClass.HUMIDITY,
        "class": SensorStateClass.MEASUREMENT
    },
    "luminance": {
        "name": "Luminance",
        "unit": LIGHT_LUX,
        "device": SensorDeviceClass.ILLUMINANCE,
        "class": SensorStateClass.MEASUREMENT
    },
    "battery": {
        "name": "Battery",
        "unit": PERCENTAGE,
        "device": SensorDeviceClass.BATTERY,
        "class": SensorStateClass.MEASUREMENT
    },
    "customEvent": {
        "name": "Trigger",
        "unit": None,
        "device": SensorDeviceClass.ENUM,
        "class": None
    },
}

ENERGY_MAP = {
    "total_kilowatt_hours": {
        "name": "Total kWh",
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.TOTAL_INCREASING
    },
    "current_wattage": {
        "name": "Current W",
        "unit": UnitOfPower.WATT,
        "device": SensorDeviceClass.POWER,
        "class": SensorStateClass.MEASUREMENT
    },
    "current_kilowatt_hours": {
        "name": "Current kWh",
        "unit": UnitOfPower.KILO_WATT,
        "device": SensorDeviceClass.POWER,
        "class": SensorStateClass.MEASUREMENT
    },
    "today_kilowatt_hours": {
        "name": "Today kWh",
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.TOTAL_INCREASING
    },
    "yesterday_kilowatt_hours": {
        "name": "Yesterday kWh",
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.TOTAL_INCREASING
    },
    "month_kilowatt_hours": {
        "name": "Month kWh",
        "unit": UnitOfEnergy.KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.TOTAL_INCREASING
    },
}
