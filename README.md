# Analytics Stats


#### Maybe in development

Sensor for data from Home Assistant Analytics

## Installation

### Install with HACS (recommended)

- Add this repo as custom repository (category `Integration`) in HACS
- Search for "Analytics Stats"
- Install as usualy

#### Install mannualy

- Copy content of `analytics_stats/custom_components/` to `custom_components/` in your Home Assistant

## Configuration

- Add configuration to `configuration.yaml`
- Restart Home Assistant

### Options
| Option | Description | Required | Example |
--- | --- | --- | ---
| countries | String of [country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) separated by space | no | `"SK CZ"` |
| integrations | String of integrations names separated by space | no | `"esphome systemmonitor"` |


#### Example configuration:
```yaml
sensor:
  - platform: analytics_stats
    countries: "SK CZ"
    integrations: "esphome systemmonitor"
```
