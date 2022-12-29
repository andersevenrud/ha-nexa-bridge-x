import logging
import aiohttp
import json

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
