# Analytics Stats


#### Still in development

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

##### Configuration:
```yaml
sensor:
  - platform: analytics_stats
```
