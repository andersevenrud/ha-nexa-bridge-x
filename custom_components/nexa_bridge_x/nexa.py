"""
Home Assistant - Nexa Bridge X Integration

Author: Anders Evenrud <andersevenrud@gmail.com>
Homepage: https://github.com/andersevenrud/ha-nexa-bridge-x
License: MIT
"""
from __future__ import annotations
from functools import reduce
from datetime import timedelta
from typing import Any
from aiohttp.web import Response
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import (
    NODE_SENSOR_CAPABILITIES,
    NODE_BINARY_CAPABILITIES,
    NODE_MEDIA_CAPABILITIES,
    POLL_INTERVAL,
    POLL_TIMEOUT
)
import asyncio
import aiohttp
import json
import logging
import async_timeout

_LOGGER = logging.getLogger(__name__)

# TODO: Add correct typing
NexaNodeValueType = str | int | float | bool
NexaEnergyData = Any
NexaEnergyNodeData = Any
NexaNodeData = Any
NexaInfoData = Any
NexaCallData = Any


def is_capable_of(node: NexaNode, items: list(str)):
    """Check if given capability is available"""
    return any(cap for cap in items if cap in node.capabilities)


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


class NexaPlatform:
    """Nexa Platform"""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        host = entry.data["host"]
        username = entry.data["username"]
        password = entry.data["username"]

        self.api = NexaApi(host, username, password)
        self.coordinator = NexaCoordinator(hass, self.api)

    async def init(self) -> None:
        """Initialize all services"""
        await self.api.test_connection()
        await self.coordinator.async_config_entry_first_refresh()


class NexaApi:
    """Nexa API"""
    host: str

    def __init__(self, host: str, username: str, password: str) -> None:
        self.host = host
        self.username = username
        self.password = password

    async def handle_response(self, response: Response) -> Any:
        """Handles response"""
        _LOGGER.debug("%s %s: %s",
                      str.upper(response.method),
                      response.url,
                      response.status)

        if not response.ok:
            text = await response.text()
            if response.status == 400:
                raise NexaApiInvalidBodyError(text)
            if response.status == 401:
                raise NexaApiAuthorizationError(text)

            raise NexaApiGeneralError(text)

        return await response.json()

    async def request(
        self,
        method: str,
        endpoint: str,
        body: Any = None
    ) -> Response:
        """Performs a request"""
        url = "http://%s/v1/%s" % (self.host, endpoint or "")
        auth = aiohttp.BasicAuth(self.username, self.password)

        async with aiohttp.ClientSession() as session:
            if method == "post":
                headers = {
                    "accept": "application/json",
                    "content-type": "application/json"
                }

                _LOGGER.debug("POST %s: %s", url, json.dumps(body))

                async with session.post(
                    url,
                    auth=auth,
                    json=body,
                    headers=headers
                ) as response:
                    return await self.handle_response(response)
            else:
                async with session.get(url, auth=auth) as response:
                    return await self.handle_response(response)

    async def test_connection(self) -> None:
        """See if the connection is valid"""
        result = await self.fetch_info()

        if "name" not in result or result["name"] != "Nexa Bridge X":
            raise NexaApiNotCompatibleError("Endpoint not compatible")

    async def fetch_info(self) -> NexaInfoData:
        """Get information about bridge"""
        return await self.request("get", "info")

    async def fetch_nodes(self) -> list[NexaNodeData]:
        """Get all configured nodes"""
        return await self.request("get", "nodes")

    async def fetch_node(self, node: str) -> NexaNodeData:
        """Get a confiured node"""
        return await self.request("get", f"nodes/{node}")

    async def fetch_energy(self) -> NexaEnergyData:
        """Get energy stats"""
        return await self.request("get", "energy")

    async def fetch_energy_nodes(self) -> NexaEnergyNodeData:
        """Get energy node stats"""
        return await self.request("get", "energy/nodes")

    async def node_call(
        self,
        node: str,
        capability: str,
        value: any
    ) -> NexaCallData:
        """Perform an action on a device"""
        body = {"capability": capability, "value": value}
        return await self.request("post", f"nodes/{node}/call", body)


class NexaInfo:
    """Model for device information"""
    name: str
    version: str
    model: str
    id: str

    def __init__(self, data: NexaInfoData):
        self.name = data["name"]
        self.version = data["version"]
        self.model = data["systemType"]
        self.id = data["gwid"]


class NexaNodeValue:
    """Model for node values"""

    def __init__(
        self,
        name: str,
        value: NexaNodeValueType,
        prev_value: NexaNodeValueType,
        time: str
    ):
        self.name = name
        self.value = value
        self.prev_value = prev_value
        self.time = time


class NexaEnergy:
    """Model for energy stats"""
    total_kilowatt_hours: float | None
    current_wattage: int | None
    current_kilowatt_hours: float | None
    today_kilowatt_hours: float | None
    yesterday_kilowatt_hours: float | None
    month_kilowatt_hours: float | None

    def __init__(
        self,
        data: NexaEnergyData,
        node_data: NexaEnergyNodeData
    ):
        self.total_kilowatt_hours = None
        self.current_wattage = None
        self.current_kilowatt_hours = None
        self.today_kilowatt_hours = None
        self.yesterday_kilowatt_hours = None
        self.month_kilowatt_hours = None

        if node_data["status"] == "OK":
            if "list" in node_data["data"]:
                self.total_kilowatt_hours = reduce(
                    lambda result, value: result + value["value"],
                    node_data["data"]["list"],
                    0
                )

        if data["status"] == "OK":
            if "current" in data["data"]:
                current = data["data"]["current"]["total"]
                self.current_wattage = current["wattage"]
                self.current_kilowatt_hours = current["kwh"]
            if "history" in data["data"]:
                history = data["data"]["history"]
                self.today_kilowatt_hours = history["today"]
                self.yesterday_kilowatt_hours = history["yesterday"]
                self.month_kilowatt_hours = history["month"]


class NexaNode:
    """Model for a node"""
    id: str
    name: str
    capabilities: list[str]
    values: list[NexaNodeValue]

    def __init__(self, node: NexaNodeData):
        values = []
        for key, data in node["lastEvents"].items():
            nv = NexaNodeValue(
                key,
                data["value"],
                data["prevValue"],
                data["time"]
            )
            values.append(nv)

        self.id = node["id"]
        self.name = node["name"]
        self.capabilities = node["capabilities"]
        self.values = values

    def get_sensor_capabilities(self) -> list[str]:
        """Get all capabilities"""
        return list(filter(
            lambda n: n in NODE_SENSOR_CAPABILITIES,
            self.capabilities
        ))

    def get_value(self, name: str) -> NexaNodeValueType | None:
        """Get current state value"""
        for value in self.values:
            if value.name == name:
                return value.value
        return None

    def is_switch(self) -> bool:
        """If this is a switch"""
        return "switchBinary" in self.capabilities

    def is_light(self) -> bool:
        """If this is a light"""
        return "switchLevel" in self.capabilities

    def is_sensor(self) -> bool:
        """If this is a sensor"""
        return is_capable_of(self, NODE_SENSOR_CAPABILITIES)

    def is_binary_sensor(self) -> bool:
        """If this is a binary sensor"""
        return is_capable_of(self, NODE_BINARY_CAPABILITIES)

    def is_media_player(self) -> bool:
        """If this is a media player"""
        return is_capable_of(self, NODE_MEDIA_CAPABILITIES)


class NexaData:
    """Model for polled data"""

    def __init__(
        self,
        info: NexaInfo,
        nodes: list[NexaNode],
        energy: NexaEnergy
    ):
        self.info = info
        self.nodes = nodes
        self.energy = energy


class NexaCoordinator(DataUpdateCoordinator):
    """Coordinates updates between entities"""

    def __init__(self, hass: HomeAssistant, api: NexaApi):
        super().__init__(
            hass,
            _LOGGER,
            name="Nexa Bridge X Coordinator",
            update_interval=timedelta(seconds=POLL_INTERVAL),
        )
        self.api = api

    def get_node_by_id(self, node_id: str) -> NexaNode | None:
        """Gets node by id"""
        if self.data.nodes:
            for node in self.data.nodes:
                if node.id == node_id:
                    return node
        return None

    async def handle_switch(
        self,
        node_id: str,
        value: bool
    ) -> None:
        """Handle a switch action"""
        await self.api.node_call(node_id, "switchBinary", value)

    async def handle_dimmer(
        self,
        node_id: str,
        value: NexaNodeValueType
    ) -> None:
        """Handle a dimmer action"""
        await self.api.node_call(node_id, "switchLevel", value)

    async def handle_media_player(
        self,
        node_id: str,
        capability: str,
        value: NexaNodeValueType
    ) -> None:
        """Handle a media player action"""
        await self.api.node_call(node_id, capability, value)

    async def _async_update_data(self) -> None:
        """Update data for all nodes in the background"""
        try:
            async with async_timeout.timeout(POLL_TIMEOUT):
                results = await asyncio.gather(*[
                    self.api.fetch_info(),
                    self.api.fetch_nodes(),
                    self.api.fetch_energy(),
                    self.api.fetch_energy_nodes(),
                ])

                (info, nodes, energy, energy_nodes) = results

                return NexaData(
                    NexaInfo(info),
                    list(map(lambda n: NexaNode(n), nodes)),
                    NexaEnergy(energy, energy_nodes)
                )
        except NexaApiAuthorizationError as err:
            raise ConfigEntryAuthFailed from err
        except NexaApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
