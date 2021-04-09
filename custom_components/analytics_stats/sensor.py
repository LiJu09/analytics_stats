"""Platform for Analytics Stats integration."""

from datetime import timedelta
import logging

import requests
#import voluptuous as vol

#from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.exceptions import PlatformNotReady
#import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle
#from homeassistant.util.dt import utcnow

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)
SCAN_INTERVAL = timedelta(seconds=600)
RETRY_INTERVAL = timedelta(seconds=30)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Analytics Stats platform."""
    data = AnalyticsStatsData(config, hass)
    if data.data is None:
        raise PlatformNotReady
    add_entities(data.devices, True)


class AnalyticsStatsSensor(SensorEntity):
    """Sensor used to display information from Home Asistant Analytics."""

    def __init__(self, data, name, icon, path, decimal):
        """Initialize an AnalyticsStatsSensor sensor."""
        self._data = data
        self._name = name
        self._icon = icon
        self.path = path
        self.decimal = decimal
        self.value = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the mdi icon of the sensor."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.value

    def update(self):
        """Update the sensor from a new JSON object."""
        self._data.update()
        latest = self._data.data[list(self._data.data.keys())[-1]]
        _LOGGER.debug("🆙 Updating %s", self._name)
        self.value = round(latest[self.path], self.decimal)


class AnalyticsStatsInstallTypesSensor(SensorEntity):
    """Sensor used to display installation types information from Home Asistant Analytics."""

    def __init__(self, data, name, icon, path, decimal):
        """Initialize an AnalyticsStatsSensor sensor."""
        self._data = data
        self._name = name
        self._icon = icon
        self.path = path
        self.decimal = decimal
        self.value = None
        self.install_types_attr = {"os": 0,
                                   "container": 0,
                                   "core": 0,
                                   "supervised": 0}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the mdi icon of the sensor."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.value

    @property
    def device_state_attributes(self):
        """Attributes."""
        return self.install_types_attr

    def update(self):
        """Update the sensor from a new JSON object."""
        self._data.update()
        latest = self._data.data[list(self._data.data.keys())[-1]]
        key_list = list(self.install_types_attr.keys())
        _LOGGER.debug("🆙 Updating %s", self._name)
        self.value = round(latest[self.path], self.decimal)
        
        for key in key_list:
            self.install_types_attr.update({key: latest["installation_types"][key]})


class AnalyticsStatsData:
    """Class used to pull data from API and create sensors."""

    def __init__(self, config, hass):
        """Initialize the Analytics Stats data-handler."""
        self.data = None
        self._config = config
        self._hass = hass
        self.devices = []
        self.initialize()

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Hit by the timer with the configured interval."""
        if self.data is None:
            self.initialize()
        else:
            self.refresh()

    def refresh(self):
        """Download and parse JSON from API."""
        data_url = "https://analytics-api.home-assistant.io/v1"

        try:
            response = requests.get(data_url, timeout=30)
            self.data = response.json()
            _LOGGER.debug("☁️ Requesting analytics data")
        except requests.exceptions.ConnectionError:
            _LOGGER.debug("ConnectionError: Is analytics-api.home-assistant.io up?")

    def initialize(self):
        """Add devices."""
        self.refresh()

        if self.data is None:
            return

        self.devices = [AnalyticsStatsInstallTypesSensor(self, "Active Installations", "mdi:home-group", "active_installations", 0),
                        AnalyticsStatsSensor(self, "Reports Statistics", "mdi:home-analytics", "reports_statistics", 0),
                        AnalyticsStatsSensor(self, "Reports Integrations", "mdi:home-plus", "reports_integrations", 0),
                        AnalyticsStatsSensor(self, "Average Addons", "mdi:puzzle", "avg_addons", 2),
                        AnalyticsStatsSensor(self, "Average Integrations", "mdi:puzzle", "avg_integrations", 2),
                        AnalyticsStatsSensor(self, "Average Entities", "mdi:shape", "avg_states", 2),
                        AnalyticsStatsSensor(self, "Average Automations", "mdi:robot", "avg_automations", 2),
                        AnalyticsStatsSensor(self, "Average Users", "mdi:account-multiple", "avg_users", 2),
        ]
