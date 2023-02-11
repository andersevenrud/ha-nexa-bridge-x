"""
Home Assistant - Nexa Bridge X Integration

Author: Anders Evenrud <andersevenrud@gmail.com>
Homepage: https://github.com/andersevenrud/ha-nexa-bridge-x
License: MIT
"""
from __future__ import annotations
from functools import reduce
from datetime import timedelta
from typing import cast, Any
from homeassistant.helpers.httpx_client import get_async_client
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
    POLL_TIMEOUT,
    RECONNECT_SLEEP,
    WS_PORT,
    HTTP_BASIC_AUTH
)
import dateutil.parser
import asyncio
import aiohttp
import json
import logging
import async_timeout
import httpx

_LOGGER = logging.getLogger(__name__)

# TODO: Add correct typing
NexaNodeValueType = str | int | float | bool
NexaEnergyData = Any
NexaLegacyEnergyData = Any
NexaEnergyNodeData = Any
NexaNodeData = Any
NexaInfoData = Any
NexaCallData = Any
NexaWebsocketMessage = str
NexaWebsocketData = Any


def is_capable_of(node: NexaNode, items: list(str)) -> bool:
    """Check if given capability is available"""
    return any(cap for cap in items if cap in node.capabilities)


def is_newer_date(current: str, new: str) -> bool:
    """Check if given timestamp is newer or equal to the current"""
    current_time = dateutil.parser.isoparse(current)
    new_time = dateutil.parser.isoparse(new)
    return new_time >= current_time


def values_from_events(node: NexaNodeData, legacy: bool) -> list[NexaNodeValue]:
    """Creates a list of node values based on node data"""
    prev_key = legacy and "value" or "prevValue"
    keys = (prev_key, "value", "time")
    ignores = ("methodCall")
    values = []

    for key, data in node["lastEvents"].items():
        if key not in ignores and all(k in data for k in keys):
            values.append(NexaNodeValue(
                key,
                data["value"],
                data[prev_key],
                data["time"]
            ))

    return values


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
        password = entry.data["password"]
        legacy = entry.data["legacy"]

        self.api = NexaApi(hass, host, username, password, legacy)
        self.coordinator = NexaCoordinator(hass, self.api, legacy)
        self.ws = NexaWebSocket(hass, host, self.coordinator)

    async def destroy(self) -> None:
        """Destroy all running services"""
        await self.ws.destroy()

    async def init(self) -> None:
        """Initialize all services"""
        await self.api.test_connection()
        await self.coordinator.async_config_entry_first_refresh()
        await self.ws.connect()


class NexaWebSocket:
    """Nexa Websocket"""
    host: str
    stopping: bool = False
    task = None
    ws: aiohttp.ws | None = None
    session: aiohttp.session | None = None

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        coordinator: NexaCoordinator
    ) -> None:
        self.hass = hass
        self.host = host
        self.coordinator = coordinator

    async def destroy(self) -> None:
        """Stop all running things"""
        self.stopping = True
        _LOGGER.debug("Destroying websocket api instance")

        await self.close()

    async def close(self) -> None:
        """Close the running session"""
        _LOGGER.debug("Closing websocket")

        if self.ws:
            await self.ws.close()
            self.ws = None

        if self.session:
            await self.session.close()
            self.session = None

        if self.task:
            self.task.cancel()
            self.task = None

    async def on_message(self, msg: NexaWebsocketMessage) -> None:
        """Handle message from websocket"""
        if not msg.startswith("{"):
            msg = msg.split(':', 1)[1]

        try:
            data = json.loads(msg)
        except Exception as err:
            _LOGGER.warning("Invalid websocket message (%s): %s", msg, err)
            return

        try:
            await self.coordinator.update_node_from_message(data)
        except Exception:
            _LOGGER.warning("Failed to handle message: %s", msg)

    async def run(self, url) -> None:
        """Create websocket connection"""
        try:
            async with aiohttp.ClientSession() as session:
                self.session = session

                try:
                    async with session.ws_connect(url) as ws:
                        self.ws = ws

                        async for msg in self.ws:
                            try:
                                if msg.type in (aiohttp.WSMsgType.CLOSED,
                                                aiohttp.WSMsgType.ERROR):
                                    break

                                if msg.data:
                                    await self.on_message(
                                        cast(NexaWebsocketMessage, msg.data)
                                    )
                            except Exception:
                                _LOGGER.error("Websocket message error")

                except Exception:
                    _LOGGER.warning("Failed to create websocket connection...")

        except Exception:
            _LOGGER.error("Failed to create websocket session...")

        asyncio.create_task(self.connect(True))

    async def connect(self, reconnect: bool = False) -> None:
        """Initiate websocket connection"""

        await self.close()

        if self.stopping:
            return

        url = f"ws://{self.host}:{WS_PORT}"

        _LOGGER.debug(
            "%s to websocket: %s",
            reconnect and "Reconnecting" or "Connecting",
            url
        )

        if reconnect:
            await asyncio.sleep(RECONNECT_SLEEP)

        self.task = asyncio.create_task(self.run(url))


class NexaApi:
    """Nexa API"""

    def __init__(
        self,
        hass: HomeAssistant,
        host: str,
        username: str,
        password: str,
        legacy: bool
    ) -> None:
        self.hass = hass
        self.host = host
        self.username = username
        self.password = password
        self.legacy = legacy
        self._client = get_async_client(hass)

    async def handle_response(self, method: str, response: httpx.Response) -> Any:
        """Handles response"""
        _LOGGER.debug("%s %s: %s",
                      str.upper(method),
                      response.url,
                      response.status_code)

        ok = response.status_code >= 200 and response.status_code < 300
        if not ok:
            if response.status_code == 400:
                raise NexaApiInvalidBodyError(response.text)
            if response.status_code == 401:
                raise NexaApiAuthorizationError(response.text)

            raise NexaApiGeneralError(response.text)

        return response.json()

    async def request(
        self,
        method: str,
        endpoint: str,
        body: Any = None
    ) -> Response:
        """Performs a request"""
        url = "http://%s/v1/%s" % (self.host, endpoint or "")

        if HTTP_BASIC_AUTH or not self.legacy:
            auth = httpx.BasicAuth(self.username, self.password)
        else:
            auth = httpx.DigestAuth(self.username, self.password)

        _LOGGER.debug("%s %s: %s", str.upper(method), url, json.dumps(body))

        response = await self._client.request(
            method,
            url,
            auth=auth,
            json=body,
        )

        return await self.handle_response(method, response)

    async def test_connection(self) -> NexaInfoData:
        """See if the connection is valid"""
        result = await self.fetch_info()

        if not result:
            raise NexaApiNotCompatibleError("Device reported no information")

        for key in ["name", "systemType", "version"]:
            if key not in result:
                raise NexaApiNotCompatibleError("Device response invalid")

        check_type = self.legacy and "Bridge1" or "Bridge2"
        check_ver = self.legacy and "1" or "2"

        if result["systemType"] != check_type:
            raise NexaApiNotCompatibleError("Device system not compatible")

        # TODO: Add semver check in the future if there are firmware diffs
        if not str(result["version"]).startswith(check_ver):
            raise NexaApiNotCompatibleError("Endpoint not compatible")

        return result

    async def fetch_info(self) -> NexaInfoData:
        """Get information about bridge"""
        return await self.request("get", "info")

    async def fetch_nodes(self) -> list[NexaNodeData]:
        """Get all configured nodes"""
        result = await self.request("get", "nodes")

        if self.legacy:
            return await asyncio.gather(*[
                self.fetch_node(r["id"]) for r in result
            ])

        return result

    async def fetch_node(self, node: str) -> NexaNodeData:
        """Get a confiured node"""
        return await self.request("get", f"nodes/{node}")

    async def fetch_energy(self) -> NexaEnergyData | NexaLegacyEnergyData:
        """Get energy stats"""
        return await self.request("get", "energy")

    async def fetch_energy_nodes(self) -> NexaEnergyNodeData | None:
        """Get energy node stats"""
        if self.legacy:
            return None

        return await self.request("get", "energy/nodes")

    async def node_call(
        self,
        node: str,
        capability: str,
        value: any
    ) -> NexaCallData:
        """Perform an action on a device"""
        if self.legacy and capability == "switchBinary":
            binaryValue = value and "turnOn" or "turnOff"
            body = {"cap": capability, "method": binaryValue}
        else:
            body = {"cap": capability, "value": value}

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
        data: NexaEnergyData | NexaLegacyEnergyData,
        node_data: NexaEnergyNodeData | None,
        legacy: bool
    ):
        self.total_kilowatt_hours = None
        self.current_wattage = None
        self.current_kilowatt_hours = None
        self.today_kilowatt_hours = None
        self.yesterday_kilowatt_hours = None
        self.month_kilowatt_hours = None

        if not legacy and data and node_data:
            self.populate(data, node_data)
        elif legacy and data:
            self.populate_legacy(data)

    def populate_legacy(
        self,
        data: NexaLegacyEnergyData
    ):
        """Populate legacy energy data from api"""
        # FIXME: What even are these values ?!
        self.current_wattage = data["kW"] / 1000
        self.total_kilowatt_hours = data["kWh"]

    def populate(
        self,
        data: NexaEnergyData,
        node_data: NexaEnergyNodeData,
    ):
        """Populate energy data from api"""
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

    def __init__(self, node: NexaNodeData, legacy: bool):
        self.id = node["id"]
        self.name = node["name"]
        self.capabilities = node["capabilities"]
        self.values = values_from_events(node, legacy)

    def get_binary_capabilities(self) -> list[str]:
        """Get all capabilities"""
        return list(filter(
            lambda n: n in NODE_BINARY_CAPABILITIES,
            self.capabilities
        ))

    def get_sensor_capabilities(self) -> list[str]:
        """Get all capabilities"""
        return list(filter(
            lambda n: n in NODE_SENSOR_CAPABILITIES,
            self.capabilities
        ))

    def set_values_from_node(self, node: NexaNode) -> None:
        """Sets values from another node"""
        for new_value in node.values:
            new_time = new_value.time
            for current_value in self.values:
                current_time = current_value.time
                if current_value.name == new_value.name:
                    if is_newer_date(current_time, new_time):
                        current_value.value = new_value.value
                        _LOGGER.debug("Patching node %s from node: %s = %s", self.id, current_value.name, new_value.value)
                    else:
                        _LOGGER.debug("Not Patching node %s from node - outdated", self.id)
                    break

    def set_value(
        self,
        name: str,
        new_value: NexaNodeValueType,
        new_time: str
    ) -> None:
        """Set current state value"""
        for value in self.values:
            if value.name == name:
                if is_newer_date(value.time, new_time):
                    value.value = new_value
                    value.time = new_time
                    _LOGGER.debug("Patching node %s with value: %s = %s", self.id, name, new_value)
                else:
                    _LOGGER.debug("Not Patching node %s from value - outdated", self.id)
                break

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

    def __init__(self, hass: HomeAssistant, api: NexaApi, legacy: bool):
        super().__init__(
            hass,
            _LOGGER,
            name="Nexa Bridge X Coordinator",
            update_interval=timedelta(seconds=POLL_INTERVAL),
        )
        self.api = api
        self.legacy = legacy

    def get_node_by_id(self, node_id: str) -> NexaNode | None:
        """Gets node by id"""
        if self.data and self.data.nodes:
            for node in self.data.nodes:
                if node.id == node_id:
                    return node
        return None

    def update_nodes_from_data(self, data: NexaData):
        """Try to update nodes from given data"""
        self.data.info = data.info
        self.data.energy = data.energy

        for node in data.nodes:
            current_node = self.get_node_by_id(node.id)
            if current_node:
                current_node.set_values_from_node(node)

    async def update_node_from_message(self, data: NexaWebsocketData) -> None:
        """Try to update a node based on message"""
        if not self.data:
            _LOGGER.info("Coordinator is not yet ready to update data...")
            return

        cap_key = self.legacy and "name" or "capability"
        keys = (cap_key, "sourceNode", "value", "time")
        if not all(k in data for k in keys):
            return

        node_id: str = data["sourceNode"]
        if node_id and str(node_id) != "-1":
            value: NexaNodeValueType = data["value"]
            time: NexaNodeValueType = data["time"]
            cap: str = data[cap_key]

            _LOGGER.debug("Coordinator update message: %s", data)

            node = self.get_node_by_id(node_id)
            if node:
                node.set_value(cap, value, time)
                self.async_set_updated_data(self.data)

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

                data = NexaData(
                    NexaInfo(info),
                    list(map(lambda n: NexaNode(n, self.legacy), nodes)),
                    NexaEnergy(energy, energy_nodes, self.legacy)
                )

                if self.data:
                    self.update_nodes_from_data(data)
                    return self.data

                return data
        except NexaApiAuthorizationError as err:
            raise ConfigEntryAuthFailed from err
        except NexaApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}")
