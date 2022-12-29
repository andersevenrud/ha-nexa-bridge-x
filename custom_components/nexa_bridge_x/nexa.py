from __future__ import annotations
from functools import reduce
from datetime import timedelta
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import NODE_SENSOR_CAPABILITIES
import asyncio
import aiohttp
import json
import logging
import async_timeout

_LOGGER = logging.getLogger(__name__)

class NexaApiError(Exception):
    """Base error"""


class NexaApiAuthorizationError(NexaApiError):
    """Authorization error"""


class NexaApiInvalidBodyError(NexaApiError):
    """Invalid body error"""


class NexaApiGeneralError(NexaApiError):
    """General error"""


class NexaApiNotCompatibleError(NexaApiError):
    """Not a Nexa API error"""

class NexaApi:
    """Nexa API"""
    def __init__(self, host: str, username: str, password: str) -> None:
        self.host = host
        self.username = username
        self.password = password

    async def handle_response(self, method, url, response):
        """Handles response"""
        _LOGGER.debug("%s %s: %s", str.upper(method), url, response.status)

        if not response.ok:
            text = await response.text()
            if response.status == 400:
                raise NexaApiInvalidBodyError(text)
            if response.status == 401:
                raise NexaApiAuthorizationError(text)

            raise NexaApiGeneralError(text)

        return await response.json()

    async def request(self, method: str, endpoint: str, body = None):
        """Performs a request"""
        url = "http://%s/v1/%s" % (self.host, endpoint or '')
        auth = aiohttp.BasicAuth(self.username, self.password)

        async with aiohttp.ClientSession() as session:
            if method == 'post':
                headers = {
                    'accept': 'application/json',
                    'content-type': 'application/json'
                }

                _LOGGER.debug("POST %s: %s", url, json.dumps(body))

                async with session.post(url, auth=auth, json=body, headers=headers) as response:
                    return await self.handle_response(method, url, response)
            else:
                async with session.get(url, auth=auth) as response:
                    return await self.handle_response(method, url, response)

    async def test_connection(self):
        """See if the connection is valid"""
        result = await self.fetch_info()
        # TODO: Check version number
        if "name" not in result or result["name"] != "Nexa Bridge X":
            raise NexaApiNotCompatibleError("Endpoint not compatible")

    async def fetch_info(self):
        """Get information about hub"""
        return await self.request('get', 'info')

    async def fetch_nodes(self):
        """Get all configured nodes"""
        return await self.request('get', 'nodes')

    async def fetch_node(self, node: str):
        """Get a confiured node"""
        return await self.request('get', f"nodes/{node}")

    async def fetch_energy(self):
        """Get energy stats"""
        return await self.request('get', "energy")

    async def fetch_energy_nodes(self):
        """Get energy node stats"""
        return await self.request('get', "energy/nodes")

    async def node_call(self, node: str, capability: str, value: any):
        """Perform an action on a device"""
        return await self.request('post', f"nodes/{node}/call", { 'capability': capability, 'value': value })

class NexaNodeValue:
    """Model for node values"""
    def __init__(self, name, value, prev_value, time):
        self.name = name
        self.value = value
        self.prev_value = prev_value
        self.time = time


class NexaEnergy:
    """Model for energy stats"""
    def __init__(self, data, node_data):
        self.total_kilowatt_hours = None
        self.current_wattage = None
        self.current_kilowatt_hours = None
        self.today_kilowatt_hours = None
        self.yesterday_kilowatt_hours = None
        self.month_kilowatt_hours = None

        if node_data["status"] == "OK":
            if "list" in node_data["data"]:
                self.total_kilowatt_hours = reduce(lambda result, value: result + value["value"], node_data["data"]["list"], 0)

        if data["status"] == "OK":
            if "current" in data["data"]:
                self.current_wattage = data["data"]["current"]["total"]["wattage"]
                self.current_kilowatt_hours = data["data"]["current"]["total"]["kwh"]
            if "history" in data["data"]:
                self.today_kilowatt_hours = data["data"]["history"]["today"]
                self.yesterday_kilowatt_hours = data["data"]["history"]["yesterday"]
                self.month_kilowatt_hours = data["data"]["history"]["month"]


class NexaNode:
    """Model for a node"""
    def __init__(self, node):
        values = []
        for key, data in node["lastEvents"].items():
            values.append(NexaNodeValue(key, data["value"], data["prevValue"], data["time"]))

        self.id = node["id"]
        self.name = node["name"]
        self.capabilities = node["capabilities"]
        self.values = values

    def get_sensor_capabilities(self):
        """Get all capabilities"""
        return list(filter(lambda n: n in NODE_SENSOR_CAPABILITIES, self.capabilities))

    def get_value(self, name):
        """Get current state value"""
        for value in self.values:
            if value.name == name:
                return value.value
        return None

    def is_switch(self):
        """If this is a switch"""
        return "switchBinary" in self.capabilities

    def is_light(self):
        """If this is a light"""
        return "switchLevel" in self.capabilities

    def is_sensor(self):
        """If this is a sensor"""
        for cap in NODE_SENSOR_CAPABILITIES:
            if cap in self.capabilities:
                return True

        return False


class NexaData:
    """Model for polled data"""
    def __init__(self, nodes, energy):
        self.nodes = nodes
        self.energy = energy

class NexaCoordinator(DataUpdateCoordinator):
    """Coordinates updates between entities"""
    def __init__(self, hass, api):
        super().__init__(
            hass,
            _LOGGER,
            name="Nexa Bridge X Coordinator",
            update_interval=timedelta(seconds=10),
        )
        self.api = api

    def get_node_by_id(self, node_id):
        """Gets node by id"""
        if self.data.nodes:
            for node in self.data.nodes:
                if node.id == node_id:
                    return node
        return None

    async def handle_switch(self, node_id, value):
        """Handle a switch action"""
        await self.api.node_call(node_id, "switchBinary", value)

    async def handle_dimmer(self, node_id, value):
        """Handle a dimmer action"""
        await self.api.node_call(node_id, "switchLevel", value)

    async def _async_update_data(self):
        """Update data for all nodes in the background"""
        try:
            async with async_timeout.timeout(10):
                results = await asyncio.gather(*[
                    self.api.fetch_nodes(),
                    self.api.fetch_energy(),
                    self.api.fetch_energy_nodes(),
                ])

                (nodes, energy, energy_nodes) = results

                return NexaData(
                    list(map(lambda n: NexaNode(n), nodes)),
                    NexaEnergy(energy, energy_nodes)
                )
        except NexaApiAuthorizationError as err:
            raise ConfigEntryAuthFailed from err
        except NexaApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
