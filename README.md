# Analytics Stats


#### Maybe in development

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
| integrations | String of integration names separated by space from URL `home-assistant.io/integrations/{name}/` | no | `"esphome"` |


#### Example configuration:
```yaml
sensor:
  - platform: analytics_stats
    countries: "SK CZ"
    integrations: "esphome"
```
