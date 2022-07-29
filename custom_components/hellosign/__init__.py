"""Integrate with HelloSign API"""
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import discovery

from hellosign_sdk import HSClient
from hellosign_sdk.utils import Forbidden, HSException

from .config_flow import try_connect

from .const import (
    CONF_TEST_MODE,
    DEFAULT_TEST_MODE,
    DOMAIN,
    CONF_ENV,
    ALLOWED_ENVS,
    DEFAULT_ENV,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.NOTIFY]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Setup up a config entry."""
    try_connect(api_key=entry.data[CONF_API_KEY], env=entry.data[CONF_ENV])

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry.data

    hass.async_create_task(
        discovery.async_load_platform(
            hass,
            Platform.NOTIFY,
            DOMAIN,
            hass.data[DOMAIN][entry.entry_id],
            hass.data[DOMAIN],
        )
    )

    return True


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up with HelloSign Integration."""
    conf = config[DOMAIN]

    def send_signature_request_handler(call):
        """Handle sending a signature request"""

        try:
            client = HSClient(api_key=conf[CONF_API_KEY], env=conf[CONF_ENV])

            files = [
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            ]
            signers = [{"name": "Dude", "email_address": "dude@dude.local"}]

            client.send_signature_request(
                test_mode=conf[CONF_TEST_MODE],
                files=None,
                file_urls=files,
                title="Hi from HA",
                message="Welcoem to our house",
                signers=signers,
            )

        except Forbidden as err:
            _LOGGER.error("Authorization not accessed: %s", err.message)

        except HSException as err:
            _LOGGER.error("Error calling hellosign API: %s", err.message)

        _LOGGER.info("HelloSign API request complete")

    hass.services.register(DOMAIN, "send", send_signature_request_handler)

    # Return boolean to indicate that initialization was successful.
    return True
