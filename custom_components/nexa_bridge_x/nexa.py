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
import asyncio
import aiohttp
import json
import logging
import async_timeout

_LOGGER = logging.getLogger(__name__)

class NexaApiError(Exception):
    pass

class NexaApiAuthorizationError(NexaApiError):
    pass


class NexaApiInvalidBodyError(NexaApiError):
    pass


class NexaApiGeneralError(NexaApiError):
    pass

class NexaApi:
    def __init__(self, host: str, username: str, password: str) -> None:
        self.host = host
        self.username = username
        self.password = password

    async def handle_response(self, method, url, response):
        _LOGGER.debug(f"{str.upper(method)} {url}: {response.status}")

        if not response.ok:
            text = await response.text()
            if response.status == 400:
                raise NexaApiInvalidBodyError(text)
            elif response.status == 401:
                raise NexaApiAuthorizationError(text)
            else:
                raise NexaApiGeneralError(text)

        return await response.json()

    async def request(self, method: str, endpoint: str, body = None):
        url = "http://%s/v1/%s" % (self.host, endpoint or '')
        auth = aiohttp.BasicAuth(self.username, self.password)

        async with aiohttp.ClientSession() as session:
            if method == 'post':
                headers = {
                    'accept': 'application/json',
                    'content-type': 'application/json'
                }

                _LOGGER.debug(f"POST {url}: {json.dumps(body)}")

                async with session.post(url, auth=auth, json=body, headers=headers) as response:
                    return await self.handle_response(method, url, response)
            else:
                async with session.get(url, auth=auth) as response:
                    return await self.handle_response(method, url, response)

    async def test_connection(self):
        await self.fetch_info()
        return True

    async def fetch_info(self):
        return await self.request('get', 'info')

    async def fetch_nodes(self):
        return await self.request('get', 'nodes')

    async def fetch_node(self, node: str):
        return await self.request('get', f"nodes/{node}")

    async def fetch_energy(self):
        return await self.request('get', "energy")

    async def fetch_energy_nodes(self):
        return await self.request('get', "energy/nodes")

    async def node_call(self, node: str, capability: str, value: any):
        return await self.request('post', f"nodes/{node}/call", { 'capability': capability, 'value': value })

class NexaNodeValue:
    def __init__(self, name, value, prevValue, time):
        self.name = name
        self.value = value
        self.prevValue = prevValue
        self.time = time


class NexaEnergy:
    def __init__(self, data, node_data):
        self.totalKilowattHours = None
        self.currentWattage = None
        self.currentKilowattHours = None
        self.todayKilowattHours = None
        self.yesterdayKilowattHours = None
        self.monthKilowattHours = None

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
