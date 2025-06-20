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

# HomeAssitant Integration unique identifier
DOMAIN = "nexa_bridge_x"

# How often to poll the bridge for updates
POLL_INTERVAL = 60

# How long to wait for a poll request to respond
POLL_TIMEOUT = 60

# How long to wait for a call to the bridge to respond
CALL_TIMEOUT = 30

# How long to wait for the initial poll request
DISCOVERY_TIMEOUT = 120

# How long for a websocket to reconnect after failure
RECONNECT_SLEEP = 5

# Nexa API username
DEFAULT_USERNAME = "nexa"

# Nexa API password
DEFAULT_PASSWORD = "nexa"

# Nexa API websocket port
WS_PORT = 8887

# Always use Basic auth instead of Digest
HTTP_BASIC_AUTH = False

# Force value enumeration instead of aggregation
# This will always be true for legacy devices
FORCE_NODE_ENUM = False

# Force always polling on legacy devices
FORCE_NODE_POLL = False

NODE_MEDIA_CAPABILITIES = [
    "mediaVolume",
    "mediaPlayPause",
    "mediaMute"
]

NODE_BINARY_CAPABILITIES = [
    "notificationPushButton",
    "notificationContact",
    "notificationMotion",
    "notificationSmoke",
    "notificationWater",
    "notificationTwilight",
    "notificationTamper",
    "notificationButton",
    "notification"
]

NODE_SENSOR_CAPABILITIES = [
    "meter",
    "power",
    "electric_voltage",
    "electric_ampere",
    "temperature",
    "humidity",
    "luminance",
    "battery",
    "customEvent",
    "motor"
]

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
    "notificationPushButton": {
        "name": "Pushbutton"
    },
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
    "motor": {
        "name": "Motor",
        "unit": None,
        "device": SensorDeviceClass.ENUM,
        "class": None,
        "options": ["up", "down", "stop"]
    }
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
