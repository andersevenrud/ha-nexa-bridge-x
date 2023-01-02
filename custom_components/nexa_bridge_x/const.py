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

RECONNECT_SLEEP = 5

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
    "switchBinary"
]

NODE_SENSOR_CAPABILITIES = [
    "switchLevel",
    "meter",
    "power",
    "electric_voltage",
    "electric_ampere",
    "temperature",
    "humidity",
    "luminance",
    "battery"
]

ENERGY_ATTRS = [
    "total_kilowatt_hours",
    "current_wattage",
    "current_kilowatt_hours",
    "today_kilowatt_hours",
    "yesterday_kilowatt_hours",
    "month_kilowatt_hours"
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
        "unit": ENERGY_KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.TOTAL_INCREASING
    },
    "power": {
        "name": "Wattage",
        "unit": POWER_WATT,
        "device": SensorDeviceClass.POWER,
        "class": SensorStateClass.MEASUREMENT
    },
    "electric_voltage": {
        "name": "Voltage",
        "unit": ELECTRIC_POTENTIAL_VOLT,
        "device": SensorDeviceClass.VOLTAGE,
        "class": SensorStateClass.MEASUREMENT
    },
    "electric_ampere": {
        "name": "Amperage",
        "unit": ELECTRIC_CURRENT_AMPERE,
        "device": SensorDeviceClass.CURRENT,
        "class": SensorStateClass.MEASUREMENT
    },
    "temperature": {
        "name": "Temperature",
        "unit": TEMP_CELSIUS,
        "device": SensorDeviceClass.TEMPERATURE,
        "class": SensorStateClass.MEASUREMENT
    },
    "humidity": {
        "name": "Temperature",
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
}

ENERGY_MAP = {
    "total_kilowatt_hours": {
        "name": "NEXA Total kWh",
        "unit": ENERGY_KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.TOTAL_INCREASING
    },
    "current_wattage": {
        "name": "NEXA Current W",
        "unit": POWER_WATT,
        "device": SensorDeviceClass.POWER,
        "class": SensorStateClass.MEASUREMENT
    },
    "current_kilowatt_hours": {
        "name": "NEXA Current kWh",
        "unit": ENERGY_KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.MEASUREMENT
    },
    "today_kilowatt_hours": {
        "name": "NEXA Today kWh",
        "unit": ENERGY_KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.TOTAL_INCREASING
    },
    "yesterday_kilowatt_hours": {
        "name": "NEXA Yesterday kWh",
        "unit": ENERGY_KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.TOTAL_INCREASING
    },
    "month_kilowatt_hours": {
        "name": "NEXA Month kWh",
        "unit": ENERGY_KILO_WATT_HOUR,
        "device": SensorDeviceClass.ENERGY,
        "class": SensorStateClass.TOTAL_INCREASING
    },
}
