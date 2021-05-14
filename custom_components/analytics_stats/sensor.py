"""Platform for Analytics Stats integration."""

from datetime import timedelta
import logging

import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.exceptions import PlatformNotReady
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=60)
SCAN_INTERVAL = timedelta(seconds=600)
RETRY_INTERVAL = timedelta(seconds=30)

CONF_COUNTRY = 'countries'
CONF_INTEGRATION = 'integrations'
CONF_BOARD = 'boards'
CONF_OS_VERSION = 'os_versions'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_COUNTRY): cv.string,
    vol.Optional(CONF_INTEGRATION): cv.string,
    vol.Optional(CONF_BOARD): cv.string,
    vol.Optional(CONF_OS_VERSION): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Analytics Stats platform."""
    countries = config.get(CONF_COUNTRY)
    integrations = config.get(CONF_INTEGRATION)
    boards = config.get(CONF_BOARD)
    os_versions = config.get(CONF_OS_VERSION)
    data = AnalyticsStatsData(config, hass, countries, integrations, boards, os_versions)
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
        _LOGGER.debug("🆙 Updating %s", self._name)
        self.value = round(self._data.data["current"][self.path], self.decimal)

class AnalyticsStatsReportsSensor(SensorEntity):
    """Sensor used to display information from Home Asistant Analytics."""

    def __init__(self, data, name, icon, path, decimal):
        """Initialize an AnalyticsStatsSensor sensor."""
        self._data = data
        self._name = name
        self._icon = icon
        self.path = path
        self.decimal = decimal
        self.value = None
        self.percentage = None

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
        return {'percentage': self.percentage}

    def update(self):
        """Update the sensor from a new JSON object."""
        self._data.update()
        _LOGGER.debug("🆙 Updating %s", self._name)
        self.value = round(self._data.data["current"][self.path], self.decimal)
        self.percentage = round((100 * self.value) / self._data.data["current"]["extended_data_from"],2)

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
        latest = self._data.data["current"]
        key_list = list(self.install_types_attr.keys())
        _LOGGER.debug("🆙 Updating %s", self._name)
        self.value = round(latest[self.path], self.decimal)
        
        for key in key_list:
            self.install_types_attr.update({key: latest["installation_types"][key]})

class AnalyticsStatsCountrySensor(SensorEntity):
    """Sensor used to display information from Home Asistant Analytics."""

    def __init__(self, data, name, icon, path):
        """Initialize an AnalyticsStatsSensor sensor."""
        self._data = data
        self._name = name
        self._icon = icon
        self.path = path
        self.value = None
        self.percentage = None

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
        return {'percentage': self.percentage}

    def update(self):
        """Update the sensor from a new JSON object."""
        self._data.update()
        _LOGGER.debug("🆙 Updating %s", self._name)
        self.value = self._data.data["current"]["countries"][self.path]
        self.percentage = round((100 * self.value) / self._data.data["current"]["extended_data_from"],2)

class AnalyticsStatsIntegrationSensor(SensorEntity):
    """Sensor used to display information from Home Asistant Analytics."""

    def __init__(self, data, name, icon, path):
        """Initialize an AnalyticsStatsSensor sensor."""
        self._data = data
        self._name = name
        self._icon = icon
        self.path = path
        self.value = None
        self.percentage = None

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
        return {'percentage': self.percentage}

    def update(self):
        """Update the sensor from a new JSON object."""
        self._data.update()
        _LOGGER.debug("🆙 Updating %s", self._name)
        self.value = self._data.data["current"]["integrations"][self.path]
        self.percentage = round((100 * self.value) / self._data.data["current"]["reports_integrations"],2)

class AnalyticsStatsOSSensor(SensorEntity):
    """Sensor used to display information from Home Asistant Analytics."""

    def __init__(self, data, name, icon, path):
        """Initialize an AnalyticsStatsSensor sensor."""
        self._data = data
        self._name = name
        self._icon = icon
        self.path = path
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
        _LOGGER.debug("🆙 Updating %s", self._name)
        self.value = self._data.data["current"]["operating_system"][self.path[0]][self.path[1]]

class AnalyticsStatsData:
    """Class used to pull data from API and create sensors."""

    def __init__(self, config, hass, countries, integrations, boards, os_versions):
        """Initialize the Analytics Stats data-handler."""
        self.data = None
        self._config = config
        self._hass = hass
        self.devices = []
        self.countries = countries
        self.integrations = integrations
        self.boards = boards
        self.os_versions = os_versions
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
        data_url = "https://analytics.home-assistant.io/data.json"

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
                        AnalyticsStatsReportsSensor(self, "Reports Statistics", "mdi:home-analytics", "reports_statistics", 0),
                        AnalyticsStatsReportsSensor(self, "Reports Integrations", "mdi:home-plus", "reports_integrations", 0),
                        AnalyticsStatsSensor(self, "Average Addons", "mdi:puzzle", "avg_addons", 2),
                        AnalyticsStatsSensor(self, "Average Integrations", "mdi:puzzle", "avg_integrations", 2),
                        AnalyticsStatsSensor(self, "Average Entities", "mdi:shape", "avg_states", 2),
                        AnalyticsStatsSensor(self, "Average Automations", "mdi:robot", "avg_automations", 2),
                        AnalyticsStatsSensor(self, "Average Users", "mdi:account-multiple", "avg_users", 2),
        ]

        if self.countries is not None:
            for country in self.countries.split(" "):
                self.devices += [AnalyticsStatsCountrySensor(self, country + " Installations", "mdi:home-group", country),]
        
        if self.integrations is not None:
            for integration in self.integrations.split(" "):
                self.devices += [AnalyticsStatsIntegrationSensor(self, integration + " Installations", "mdi:puzzle", integration),]

        if self.boards is not None:
            for board in self.boards.split(" "):
                self.devices += [AnalyticsStatsOSSensor(self, "Installations on " + board, "mdi:server", ["boards", board]),]

        if self.os_versions is not None:
            for os_version in self.os_versions.split(" "):
                self.devices += [AnalyticsStatsOSSensor(self, os_version + " OS Installations", "mdi:server", ["versions", os_version]),]
