from __future__ import annotations
from functools import reduce
from datetime import timedelta
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import (
    DOMAIN,
    NODE_SENSOR_CAPABILITIES
)
from .api import (
    NexaApi,
    NexaApiError,
    NexaApiAuthorizationError
)
import asyncio
import logging
import async_timeout

_LOGGER = logging.getLogger(__name__)

class NexaNodeValue:
    def __init__(self, name, value, prevValue, time):
        self.name = name
        self.value = value
        self.prevValue = prevValue
        self.time = time


class NexaEnergy:
    def __init__(self, data, node_data):
        self.totalKilowattHours = 0
        self.currentWattage = 0
        self.currentKilowattHours = 0
        self.todayKilowattHours = 0
        self.yesterdayKilowattHours = 0
        self.monthKilowattHours = 0

        if node_data["status"] == "OK":
            if "list" in node_data["data"]:
                self.totalKilowattHours = reduce(lambda result, value: result + value["value"], node_data["data"]["list"], 0)

        if data["status"] == "OK":
            if "current" in data["data"]:
                self.currentWattage = data["data"]["current"]["total"]["wattage"]
                self.currentKilowattHours = data["data"]["current"]["total"]["kwh"]
            if "history" in data["data"]:
                self.todayKilowattHours = data["data"]["history"]["today"]
                self.yesterdayKilowattHours = data["data"]["history"]["yesterday"]
                self.monthKilowattHours = data["data"]["history"]["month"]


class NexaNode:
    def __init__(self, node):
        values = []
        for n, e in node["lastEvents"].items():
            values.append(NexaNodeValue(n, e["value"], e["prevValue"], e["time"]))

        self.id = node["id"]
        self.name = node["name"]
        self.capabilities = node["capabilities"]
        self.values = values

    def get_sensor_capabilities(self):
        return list(filter(lambda n: n in NODE_SENSOR_CAPABILITIES, self.capabilities))

    def get_value(self, name):
        for v in self.values:
            if v.name == name:
                return v.value
        return None

    def is_switch(self):
        return "switchBinary" in self.capabilities

    def is_light(self):
        return "switchLevel" in self.capabilities

    def is_sensor(self):
        for c in NODE_SENSOR_CAPABILITIES:
            if c in self.capabilities:
                return True

        return False


class NexaData:
    def __init__(self, nodes, energy):
        self.nodes = nodes
        self.energy = energy

class NexaCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api):
        super().__init__(
            hass,
            _LOGGER,
            name="Nexa Bridge X Coordinator",
            update_interval=timedelta(seconds=10),
        )
        self.api = api

    def get_node_by_id(self, id):
        if self.data.nodes:
            for node in self.data.nodes:
                if node.id == id:
                    return node
        return None

    async def handle_switch(self, id, value):
        await self.api.node_call(id, "switchBinary", value)

    async def handle_dimmer(self, id, value):
        await self.api.node_call(id, "switchLevel", value)

    async def _async_update_data(self):
        try:
            async with async_timeout.timeout(10):
                nodes = await self.api.fetch_nodes()
                energy = await self.api.fetch_energy()
                energy_nodes = await self.api.fetch_energy_nodes()

                return NexaData(
                    list(map(lambda n: NexaNode(n), nodes)),
                    NexaEnergy(energy, energy_nodes)
                )
        except NexaApiAuthorizationError as err:
            raise ConfigEntryAuthFailed from err
        except NexaApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
