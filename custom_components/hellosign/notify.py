"""HelloSign notify platform"""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_TARGET,
    BaseNotificationService,
)

from hellosign_sdk import HSClient
from hellosign_sdk.utils import Forbidden, HSException

_LOGGER = logging.getLogger(__name__)

async def async_get_service(

)




class HelloSignNotificationServcie(BaseNotificationService):
    """Implement the notification service for HelloSign"""

    def __init__(self, hass: HomeAssistant, api_key: str, env: str) -> None:
        """Initialize the service."""
        self.api_key = api_key
        self.hass = hass
        self.api_key = api_key
        self.env = env

    def async_send_message(self, message: str, **kwargs: Any) -> None:
        """Handle sending a signature request"""

        try:
            client = HSClient(api_key=self.api_key, env=self.env)

            files = [
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            ]
            signers = [{"name": "Dude", "email_address": "dude@dude.local"}]


            client.send_signature_request(
                test_mode=1,
                files=None,
                file_urls=files,
                title="Hi from HA",
                message="Welcoem to ouwr house",
                signers=signers,
            )

        except Forbidden as err:
            _LOGGER.error("Authorization not accessed: %s", err.message)

        except HSException as err:
            _LOGGER.error("Error calling hellosign API: %s", err.message)

        _LOGGER.info("HelloSign API request complete")

