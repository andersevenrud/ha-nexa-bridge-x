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
from .const import (
    DOMAIN,
    DEFAULT_USERNAME,
    DEFAULT_PASSWORD,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Required("username", default=DEFAULT_USERNAME): str,
        vol.Required("password", default=DEFAULT_PASSWORD): str,
        vol.Required("legacy", default=False): bool,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    try:
        api = NexaApi(hass, data["host"], data["username"], data["password"], data["legacy"])
        info = await api.test_connection()
    except Exception:
        raise InvalidAuth

    return {"title": info["name"]}


class NexaBridgeXFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Nexa Bridge X."""

    VERSION = 1

    _discovered_name: str | None = None
    _discovered_host: str | None = None
    _discovered_username: str | None = None
    _discovered_password: str | None = None
    _discovered_legacy: bool = False

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=STEP_USER_DATA_SCHEMA
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
        username: str = DEFAULT_USERNAME
        password: str = DEFAULT_PASSWORD
        is_legacy: bool = "nexabridge2" not in uid

        await self.async_set_unique_id(uid.upper())

        self._abort_if_unique_id_configured(updates={
            "host": host
        })

        try:
            api = NexaApi(self.hass, host, 'nexa', 'nexa', is_legacy)
            info = await api.test_connection()
        except Exception:  # pylint: disable=broad-except
            return self.async_abort(reason="unknown")

        self._discovered_name = info["name"]
        self._discovered_host = host
        self._discovered_username = username
        self._discovered_password = password
        self._discovered_legacy = is_legacy

        self._set_confirm_only()

        self.context["title_placeholders"] = {
            "host": host,
            "username": username,
            "password": password,
            "legacy": is_legacy,
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
            "legacy": self._discovered_legacy,
        }

        if user_input is None:
            self.context["title_placeholders"] = form

            return self.async_show_form(
                step_id="discovery_confirm",
                description_placeholders=form
            )

        return self.async_create_entry(
            title=self._discovered_name,
            data=form
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
