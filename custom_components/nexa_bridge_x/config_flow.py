"""
Home Assistant - Nexa Bridge X Integration

Author: Anders Evenrud <andersevenrud@gmail.com>
Homepage: https://github.com/andersevenrud/ha-nexa-bridge-x
License: MIT
"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components import zeroconf
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .nexa import NexaApi
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Required("username"): str,
        vol.Required("password"): str,
    }
)


class PlaceholderHub:
    def __init__(self, host: str) -> None:
        self.host = host

    async def authenticate(self, username: str, password: str) -> bool:
        try:
            api = NexaApi(self.host, username, password)
            await api.test_connection()
        except Exception:  # pylint: disable=broad-except
            return False


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    hub = PlaceholderHub(data["host"])

    if not await hub.authenticate(data["username"], data["password"]):
        raise InvalidAuth

    return {"title": "Nexa Bridge X"}


class NexaBridgeXFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nexa Bridge X."""

    VERSION = 1

    _discovered_host: str | None = None
    _discovered_username: str | None = None
    _discovered_password: str | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(
                title=info["title"],
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors
        )

    async def async_step_zeroconf(
        self,
        discovery_info: zeroconf.ZeroconfServiceInfo
    ) -> FlowResult:
        """Start a discovery flow from zeroconf."""
        uid: str = discovery_info.hostname
        host: str = discovery_info.host
        username: str = "nexa"
        password: str = "nexa"

        await self.async_set_unique_id(uid.upper())

        self._abort_if_unique_id_configured(updates={
            "host": host
        })

        try:
            api = NexaApi(host, 'nexa', 'nexa')
            await api.test_connection()
        except Exception:  # pylint: disable=broad-except
            return self.async_abort(reason="unknown")

        self._discovered_host = host
        self._discovered_username = username
        self._discovered_password = password

        self._set_confirm_only()

        self.context["title_placeholders"] = {
            "host": host,
            "username": username,
            "password": password
        }

        return await self.async_step_discovery_confirm()

    async def async_step_discovery_confirm(
        self,
        user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm the discover flow."""
        assert self._discovered_host is not None

        form = {
            "host": self._discovered_host,
            "username": self._discovered_username,
            "password": self._discovered_password,
        }

        if user_input is None:
            self.context["title_placeholders"] = form

            return self.async_show_form(
                step_id="discovery_confirm",
                description_placeholders=form
            )

        return self.async_create_entry(
            title="Nexa Bridge X",
            data=form
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
