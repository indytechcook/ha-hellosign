"""Config Flow for HelloSign"""
from __future__ import annotations

import voluptuous as vol
import logging

from homeassistant.config_entries import ConfigFlow

from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.selector import selector

from homeassistant.const import CONF_API_KEY

from hellosign_sdk import HSClient
from hellosign_sdk.utils import Forbidden, HSException, Unauthorized

from .const import (
    DOMAIN,
    CONF_ENV,
    ALLOWED_ENVS,
    DEFAULT_ENV,
    ENV_PRODUCTION,
)

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = {
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_ENV, default=DEFAULT_ENV): selector(
        {"select": {"options": ALLOWED_ENVS}}
    ),
}


class HelloSignConfigFlow(ConfigFlow, domain=DOMAIN):
    """Config flow for HelloSign"""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> FlowResult:

        errors = {}

        if user_input is not None:
            success, error_msg, client = try_connect(
                api_key=user_input[CONF_API_KEY], env=user_input[CONF_ENV]
            )

            if success:
                await self.hass.async_add_executor_job(client.get_account_info)
                return self.async_create_entry(
                    title=client.account.email_address, data=user_input
                )

            if error_msg is not None:
                errors["base"] = error_msg

        user_input = user_input or {}
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(DATA_SCHEMA), errors=errors
        )


def try_connect(
    api_key: str, env: str = ENV_PRODUCTION
) -> tuple[bool, str | None, HSClient | None]:
    """Attempt a connection to HelloSign"""

    _LOGGER.warning("Env: %s", env)
    try:
        client = HSClient(api_key=api_key, env=env)

    except Forbidden as err:
        return False, err.message, None

    except Unauthorized as err:
        return False, err.message, None

    except HSException as err:
        return False, err.message, None

    return True, None, client
