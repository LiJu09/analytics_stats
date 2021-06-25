# Analytics Stats

[![CodeFactor](https://www.codefactor.io/repository/github/liju09/analytics_stats/badge)](https://www.codefactor.io/repository/github/liju09/analytics_stats)

Sensor for data from Home Assistant Analytics

## Installation

### Install with HACS (recommended)

- Add this repo as custom repository (category `Integration`) in HACS
- Search for "Analytics Stats"
- Install as usualy

#### Install mannualy

- Copy `custom_components/analytics_stats` to `custom_components/analytics_stats` in your Home Assistant

## Configuration

- Add configuration to `configuration.yaml`
- Restart Home Assistant

### Options
| Option | Description | Required | Example |
--- | --- | --- | ---
| countries | String of [country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) separated by space | no | `"SK CZ"` |
| integrations | String of integration names separated by space from URL `home-assistant.io/integrations/{name}/` | no | `"esphome systemmonitor"` |
| boards | String of board names from [data.json](https://analytics.home-assistant.io/data.json) `current -> operating_system -> boards` | no | `"rpi4-64 rpi4"` |
| os_versions | String of OS versions from [data.json](https://analytics.home-assistant.io/data.json) `current -> operating_system -> versions` | no | `"5.13 6.0.rc1"` |

#### Example configuration:
```yaml
sensor:
  - platform: analytics_stats
    countries: "SK CZ"
    integrations: "esphome systemmonitor"
    boards: "rpi4-64 rpi4"
    os_versions: "5.13 6.0.rc1"
```
