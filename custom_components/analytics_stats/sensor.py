"""Platform for Analytics Stats integration."""
import logging
import json
import async_timeout
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

URL = "https://analytics-api.home-assistant.io/v1"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup sensor platform."""
    session = async_create_clientsession(hass)
    async_add_entities([AnalyticsStatsSensor(session, "Analytics Stats")], True)


class AnalyticsStatsSensor(Entity):
    """Analytics Stats Sensor class"""

    def __init__(self, session, name):
        self._state = None
        self._name = name
        self.session = session
        self.active_installations = 0
        self.avg_users = 0
        self.avg_automations = 0
        self.avg_integrations = 0
        self.avg_addons = 0
        self.avg_states = 0

    async def async_update(self):
        """Update sensor."""
        try:
            async with async_timeout.timeout(10, loop=self.hass.loop):
                response = await self.session.get(URL)
                info = await response.text()
            data = json.loads(info)
            latest = data[list(data.keys())[-1]]
            self._state = "OK" if response.status == 200 else "KO"
            self.active_installations = latest["active_installations"]
            self.avg_users = round(latest["avg_users"], 2)
            self.avg_automations = round(latest["avg_automations"], 2)
            self.avg_integrations = round(latest["avg_integrations"], 2)
            self.avg_addons = round(latest["avg_addons"], 2)
            self.avg_states = round(latest["avg_states"], 2)

        except Exception as error:
            _LOGGER.debug("%s - Could not update: %s", self._name, error)

    @property
    def name(self):
        """Name."""
        return self._name

    @property
    def state(self):
        """State."""
        return self._state

    @property
    def device_state_attributes(self):
        """Attributes."""
        return {
            "active_installations": self.active_installations,
            "average_addons": self.avg_addons,
            "average_integrations": self.avg_integrations,
            "average_entities": self.avg_states,
            "average_automations": self.avg_automations,
            "average_users": self.avg_users,
        }
