# Open-Meteo Weather Addon - Complete Settings Guide

A comprehensive guide to configuring the `weather.openmeteo` Kodi addon, with detailed explanations of all settings, threshold recommendations for different climates, and best practices for alert configuration.

---

## Table of Contents

1. [Introduction](#introduction)
2. [How the Addon Works](#how-the-addon-works)
3. [Location Settings](#location-settings)
4. [Unit Settings](#unit-settings)
5. [Map Settings](#map-settings)
6. [Understanding the Alert System](#understanding-the-alert-system)
7. [Weather Alerts - Detailed Guide](#weather-alerts---detailed-guide)
   - [Temperature Alerts](#temperature-alerts)
   - [Precipitation Alerts](#precipitation-alerts)
   - [Weather Condition Alerts (WMO Codes)](#weather-condition-alerts-wmo-codes)
   - [Wind Speed Alerts](#wind-speed-alerts)
   - [Wind Gust Alerts](#wind-gust-alerts)
   - [UV Index Alerts](#uv-index-alerts)
   - [Humidity Alerts](#humidity-alerts)
   - [Pressure Alerts](#pressure-alerts)
   - [Visibility Alerts](#visibility-alerts)
   - [Feels Like Temperature Alerts](#feels-like-temperature-alerts)
   - [Dewpoint Alerts](#dewpoint-alerts)
   - [Cloudiness Alerts](#cloudiness-alerts)
   - [Solar Radiation Alerts](#solar-radiation-alerts)
8. [Air Quality Alerts - Detailed Guide](#air-quality-alerts---detailed-guide)
9. [Pollen Alerts - Detailed Guide](#pollen-alerts---detailed-guide)
10. [Alert Timing and Display Settings](#alert-timing-and-display-settings)
11. [WMO Weather Code Complete Reference](#wmo-weather-code-complete-reference)
12. [Regional Threshold Recommendations](#regional-threshold-recommendations)
13. [Use Case Examples](#use-case-examples)
14. [Troubleshooting](#troubleshooting)
15. [Advanced Configuration](#advanced-configuration)
16. [Frequently Asked Questions](#frequently-asked-questions)
17. [File Locations](#file-locations)
18. [Credits and Data Sources](#credits-and-data-sources)

---

## Introduction

The Open-Meteo Weather addon for Kodi provides comprehensive weather forecasting with support for:

- Current conditions and multi-day forecasts (up to 12 days)
- Interactive weather maps (radar, satellite, temperature, wind)
- Air quality monitoring (AQI, particulate matter, pollutants)
- Pollen forecasts (Europe only)
- Customizable weather alerts and notifications
- Graph support for visual weather data (requires skin support)

This guide focuses primarily on the settings.xml configuration file, which controls all aspects of the addon's behavior. While many settings can be adjusted through Kodi's addon settings interface, understanding the underlying XML structure allows for more precise control and easier backup/restore of your configuration.

### Why Configure Alerts?

Weather alerts help you stay informed about conditions that may affect your daily activities, travel plans, or safety. However, poorly configured alerts can be annoying—triggering notifications for every light rain shower or mild temperature change. This guide will help you configure alerts that are meaningful for your specific location and needs.

---

## How the Addon Works

### Data Flow

1. **Weather Data Retrieval**: The addon fetches weather data from Open-Meteo's API based on your configured location coordinates
2. **Map Generation**: Radar and satellite imagery is retrieved from RainViewer, temperature/wind maps from weather.gc.ca and met.no
3. **Alert Processing**: Every `alert_interval` minutes (default: 30), the addon checks forecasted conditions for the next `alert_hours` hours (default: 8)
4. **Threshold Comparison**: Current and forecasted values are compared against your configured thresholds
5. **Notification Display**: If thresholds are exceeded and the corresponding alert level is enabled, a notification is displayed for `alert_duration` seconds

### Background Service

The addon runs a background service (`service.py`) that:
- Periodically refreshes weather data
- Monitors for alert conditions
- Updates window properties for skin integration
- Manages map layer downloads and caching

---

## Location Settings

The addon supports up to 5 locations. Each location has a set of associated settings.

### Location Setting Reference

| Setting | Type | Description |
|---------|------|-------------|
| `loc[N]` | string | Full location name (city, region, country) as returned by the geocoding service |
| `loc[N]user` | string | Custom display name you can set to override the default |
| `loc[N]alert` | boolean | Whether to generate alerts for this location |
| `loc[N]utz` | boolean | Use the location's local timezone for time displays |
| `loc[N]tz` | string | Timezone identifier in IANA format |
| `loc[N]lat` | float | Latitude coordinate (decimal degrees, positive = North) |
| `loc[N]lon` | float | Longitude coordinate (decimal degrees, positive = East) |

### Internal/Cache Settings

These settings are managed by the addon and should generally not be edited manually:

| Setting | Description |
|---------|-------------|
| `loc[N]data` | Timestamp of last weather data update |
| `loc[N]map` | Timestamp of last map update |
| `loc[N]rv` | Timestamp of last RainViewer update |
| `loc[N]gc` | Timestamp of last weather.gc.ca update |

### Example Location Configuration

```xml
<!-- Primary location: Amsterdam -->
<setting id="loc1">Amsterdam, North Holland, NL</setting>
<setting id="loc1user">Home</setting>
<setting id="loc1alert">true</setting>
<setting id="loc1utz">false</setting>
<setting id="loc1tz">Europe/Amsterdam</setting>
<setting id="loc1lat">52.3676</setting>
<setting id="loc1lon">4.9041</setting>

<!-- Secondary location: Vacation home -->
<setting id="loc2">Nice, Provence-Alpes-Côte d'Azur, FR</setting>
<setting id="loc2user">Vacation</setting>
<setting id="loc2alert">true</setting>
<setting id="loc2utz">true</setting>
<setting id="loc2tz">Europe/Paris</setting>
<setting id="loc2lat">43.7102</setting>
<setting id="loc2lon">7.2620</setting>
```

### Tips for Location Settings

- **Custom names**: Use `loc[N]user` to set short, recognizable names like "Home", "Work", or "Parents"
- **Timezone handling**: Enable `loc[N]utz` if you want forecast times shown in the location's local time (useful for locations in different timezones)
- **Alert management**: Disable alerts for locations you monitor casually by setting `loc[N]alert` to `false`
- **Coordinates**: For precise forecasts, use coordinates for your exact address rather than city center. You can find coordinates using Google Maps (right-click → "What's here?")

---

## Unit Settings

The addon supports extensive unit customization to match your regional preferences or personal needs.

### Temperature Units

| Setting Value | Unit | Description |
|---------------|------|-------------|
| `app` | — | Use Kodi's regional setting |
| `°C` | Celsius | Standard metric (used by most of the world) |
| `°F` | Fahrenheit | Used in USA, some Caribbean nations |
| `K` | Kelvin | Scientific absolute scale |
| `°Ré` | Réaumur | Historical scale (France) |
| `°Ra` | Rankine | Absolute scale based on Fahrenheit |
| `°Rø` | Rømer | Historical scale (Denmark) |
| `°D` | Delisle | Historical scale (inverted) |
| `°N` | Newton | Historical scale |

### Speed Units

| Setting Value | Unit | Common Usage |
|---------------|------|--------------|
| `app` | — | Use Kodi's regional setting |
| `km/h` | Kilometers per hour | Metric countries |
| `mph` | Miles per hour | UK, USA |
| `m/s` | Meters per second | Scientific, some European countries |
| `kts` | Knots | Maritime, aviation |
| `Beaufort` | Beaufort scale | Maritime (0-12 scale) |
| `m/min` | Meters per minute | Rare |
| `ft/h` | Feet per hour | Rare |
| `ft/min` | Feet per minute | Rare |
| `ft/s` | Feet per second | Rare |
| `inch/s` | Inches per second | Rare |
| `yard/s` | Yards per second | Rare |
| `Furlong/Fortnight` | — | Humorous unit |

### Precipitation Units

| Setting Value | Unit | Description |
|---------------|------|-------------|
| `mm` | Millimeters | Standard metric |
| `cm` | Centimeters | Sometimes used for snow |
| `inches` | Inches | Used in USA, UK |

### Distance Units

| Setting Value | Unit | Common Usage |
|---------------|------|--------------|
| `m` | Meters | Short distances |
| `km` | Kilometers | Metric countries |
| `mi` | Miles | UK, USA |

### Pressure Units

| Setting Value | Unit | Common Usage |
|---------------|------|--------------|
| `hPa` | Hectopascals | Standard meteorological unit (= mbar) |
| `kPa` | Kilopascals | Scientific |
| `mmHg` | Millimeters of mercury | Medical, some countries |
| `inHg` | Inches of mercury | USA aviation/weather |
| `psi` | Pounds per square inch | Industrial |

### Decimal Places

Each unit type has an associated decimal places setting (`unit[X]dp`) that controls precision:

| Setting | Controls | Recommended |
|---------|----------|-------------|
| `unittempdp` | Temperature display | 0-1 |
| `unitspeeddp` | Wind speed display | 0-1 |
| `unitprecipdp` | Precipitation display | 1 |
| `unitdistancedp` | Visibility display | 0-1 |
| `unitpressuredp` | Pressure display | 0 |
| `unitparticlesdp` | PM2.5/PM10 display | 0-1 |
| `unitpollendp` | Pollen count display | 0 |
| `unituvindexdp` | UV index display | 0-1 |
| `unitradiationdp` | Solar radiation display | 0 |

### Decimal Separator

| Setting Value | Character | Usage |
|---------------|-----------|-------|
| `.` | Period | USA, UK, most of Asia |
| `,` | Comma | Continental Europe, South America |

---

## Map Settings

The addon provides several types of weather maps that can be displayed in supported skins.

### Map Configuration Options

| Setting | Type | Range | Description |
|---------|------|-------|-------------|
| `mapzoom` | integer | 1-15 | Zoom level (higher = more detail, smaller area) |
| `maphistory` | integer | 1-24 | Hours of historical map data to store for animations |
| `maprvradar` | boolean | — | Enable RainViewer precipitation radar |
| `maprvsatellite` | boolean | — | Enable RainViewer infrared satellite |
| `mapgctemp` | boolean | — | Enable temperature overlay map |
| `mapgcwind` | boolean | — | Enable wind overlay map |
| `maposm` | boolean | — | Enable OpenStreetMap base layer |

### Zoom Level Guide

| Zoom | Coverage | Best For |
|------|----------|----------|
| 4-5 | Continental | Overview of weather systems |
| 6-7 | Regional | Multi-country view |
| 8-9 | Area | Single country / large region |
| 10-11 | Local | City and surroundings |
| 12+ | Detailed | Neighborhood level |

**Recommendation**: Zoom level 8 works well for most users, providing a good balance between detail and coverage.

### Map Data Sources

- **RainViewer**: Provides near-real-time precipitation radar and infrared satellite imagery with global coverage
- **weather.gc.ca**: Canadian government weather service (temperature and wind maps)
- **met.no**: Norwegian Meteorological Institute (additional weather data)

---

## Understanding the Alert System

The alert system is the most complex part of the addon configuration. Understanding how it works is essential for effective customization.

### Alert Levels

The addon uses a three-tier alert system:

| Level | Color | Meaning | When to Use |
|-------|-------|---------|-------------|
| **Notice** | Yellow | Informational | Weather worth noting but not concerning |
| **Caution** | Orange | Advisory | Weather may affect plans, be prepared |
| **Danger** | Red/Crimson | Warning | Severe weather, take protective action |

### Alert Setting Structure

Every alert type follows a consistent pattern with these settings:

```xml
<!-- Master switch for this alert type -->
<setting id="alert_[TYPE]_enabled">true</setting>

<!-- Which levels should trigger notifications -->
<setting id="alert_[TYPE]_notice">false</setting>
<setting id="alert_[TYPE]_caution">false</setting>
<setting id="alert_[TYPE]_danger">true</setting>

<!-- Threshold values for each level -->
<setting id="alert_[TYPE]_high_1">value</setting>  <!-- Notice threshold -->
<setting id="alert_[TYPE]_high_2">value</setting>  <!-- Caution threshold -->
<setting id="alert_[TYPE]_high_3">value</setting>  <!-- Danger threshold -->
```

### Threshold Logic Explained

#### For "High" Metrics (higher values = more severe)

Examples: Temperature high, precipitation, wind speed, UV index

```
Value < high_1           → No alert (normal)
high_1 ≤ Value < high_2  → Notice level
high_2 ≤ Value < high_3  → Caution level
Value ≥ high_3           → Danger level
```

**Visual representation:**
```
Normal    |  Notice   |  Caution  |  Danger
──────────┼───────────┼───────────┼──────────→
          high_1     high_2      high_3
```

#### For "Low" Metrics (lower values = more severe)

Examples: Temperature low, visibility

```
Value > low_1           → No alert (normal)
low_2 < Value ≤ low_1   → Notice level
low_3 < Value ≤ low_2   → Caution level
Value ≤ low_3           → Danger level
```

**Visual representation:**
```
←──────────┼───────────┼───────────┼──────────
  Danger   |  Caution  |  Notice   |  Normal
          low_3      low_2       low_1
```

### Selective Alert Levels

You can enable only the alert levels you care about. Common configurations:

| Configuration | notice | caution | danger | Result |
|---------------|--------|---------|--------|--------|
| Danger only | false | false | true | Only severe weather alerts |
| Caution and up | false | true | true | Moderate and severe alerts |
| All alerts | true | true | true | Full notification coverage |
| Disabled | false | false | false | No notifications (but data still tracked) |

**Tip**: Even with notification levels disabled, the alert data is still available to skins that support displaying alert status visually.

### Alert Timing Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `alert_hours` | 8 | How many hours ahead to check for alert conditions |
| `alert_interval` | 30 | Minutes between alert checks |
| `alert_duration` | 15 | Seconds to display notification popup |

#### How `alert_hours` Affects Different Metrics

- **Instantaneous metrics** (temperature, wind, UV): Checks each hour in the window, alerts on worst value
- **Cumulative metrics** (precipitation): Sums values across the entire window
- **Condition codes**: Checks each hour, alerts on most severe condition found

**Example**: With `alert_hours` set to 8:
- Precipitation alert checks the **total** precipitation expected in the next 8 hours
- Temperature alert checks each hour and alerts if **any** hour exceeds the threshold
- Condition alert triggers if **any** hour has a severe weather code

---

## Weather Alerts - Detailed Guide

### Temperature Alerts

Temperature alerts help you prepare for extreme heat or cold that may affect health, outdoor activities, or infrastructure.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_temperature_high_1/2/3` | High temperature thresholds |
| `alert_temperature_low_1/2/3` | Low temperature thresholds |

#### Understanding Temperature Thresholds

**High temperature considerations:**
- Body stress begins around 28-30°C for most people
- Heat warnings typically issued at 32-35°C
- Dangerous heat (risk of heat stroke) at 38°C+
- Infrastructure stress (rail buckling, power grid) at 35°C+

**Low temperature considerations:**
- Frost risk below 0°C (affects plants, pipes)
- Significant cold stress below -5°C
- Dangerous cold (frostbite risk) below -15°C
- Extreme cold (life-threatening) below -25°C

#### Regional Examples

| Region | high_1 | high_2 | high_3 | low_1 | low_2 | low_3 |
|--------|--------|--------|--------|-------|-------|-------|
| Northern Europe | 25 | 30 | 35 | -5 | -15 | -25 |
| Western Europe | 28 | 33 | 38 | -5 | -10 | -15 |
| Mediterranean | 32 | 37 | 42 | 0 | -5 | -10 |
| Southern USA | 35 | 38 | 42 | 0 | -5 | -10 |
| Northern USA | 30 | 35 | 38 | -10 | -20 | -30 |
| Tropical | 33 | 36 | 40 | 15 | 10 | 5 |

### Precipitation Alerts

Precipitation alerts warn about rainfall or snowfall that may cause flooding, travel disruption, or other impacts.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_precipitation_high_1/2/3` | Precipitation amount thresholds (in configured unit) |
| `alert_precipitationprobability_high_1/2/3` | Precipitation probability thresholds (percentage) |

#### Understanding Precipitation Amounts

Precipitation is measured as the depth of water that would accumulate on a flat surface. The alert checks the **cumulative** amount over the `alert_hours` window.

**Rainfall intensity reference:**
| Intensity | mm/hour | mm/8 hours | Impact |
|-----------|---------|------------|--------|
| Light | <2.5 | <20 | Minimal |
| Moderate | 2.5-7.5 | 20-60 | Wet conditions |
| Heavy | 7.5-50 | 60-100 | Flooding possible |
| Violent | >50 | >100 | Flash flooding likely |

**Regional context matters:**
- Desert regions: 10mm is significant
- Temperate regions: 20-30mm is notable
- Tropical regions: 50mm+ may be routine in monsoon season

#### Recommended Thresholds by Climate

| Climate Type | high_1 | high_2 | high_3 | Notes |
|--------------|--------|--------|--------|-------|
| Arid/Desert | 5 | 10 | 20 | Flash flood risk |
| Mediterranean | 10 | 25 | 50 | Autumn storms |
| Temperate Maritime | 15 | 30 | 50 | Year-round rain |
| Temperate Continental | 15 | 30 | 50 | Summer storms |
| Tropical | 30 | 60 | 100 | Monsoon-adjusted |

### Weather Condition Alerts (WMO Codes)

Weather condition alerts use standardized WMO (World Meteorological Organization) codes to identify specific weather phenomena. This is the most nuanced alert type.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_condition_wmo_1` | Space-separated WMO codes for Notice level |
| `alert_condition_wmo_2` | Space-separated WMO codes for Caution level |
| `alert_condition_wmo_3` | Space-separated WMO codes for Danger level |

#### How Condition Alerts Work

1. The addon checks each hour in the `alert_hours` window
2. For each hour, it gets the WMO weather code
3. It finds the highest severity level among all codes found
4. If that level's notifications are enabled, an alert is shown

#### Default Configuration Explained

```xml
<setting id="alert_condition_wmo_1">45 48 51 56 61 66 71 77 80 85</setting>
<setting id="alert_condition_wmo_2">53 63 73 81</setting>
<setting id="alert_condition_wmo_3">55 57 65 67 75 82 86 95 96 99</setting>
```

**Notice level (wmo_1)** - Minor weather events:
- 45, 48: Fog conditions (visibility reduction)
- 51, 56: Light drizzle (may need umbrella)
- 61, 66: Light rain (outdoor activities affected)
- 71, 77: Light snow (travel caution)
- 80, 85: Light showers (brief wet periods)

**Caution level (wmo_2)** - Moderate weather events:
- 53: Moderate drizzle
- 63: Moderate rain
- 73: Moderate snow
- 81: Moderate showers

**Danger level (wmo_3)** - Severe weather events:
- 55, 57: Heavy/freezing drizzle (ice risk)
- 65, 67: Heavy/freezing rain (flooding, ice)
- 75: Heavy snow (travel dangerous)
- 82: Violent showers (flash flooding)
- 86: Heavy snow showers
- 95, 96, 99: Thunderstorms (lightning, hail)

#### Customization Strategies

**Minimal alerts (severe only):**
```xml
<setting id="alert_condition_wmo_3">75 82 95 96 99</setting>
```
Only alerts for: heavy snow, violent showers, thunderstorms

**Winter-focused alerts:**
```xml
<setting id="alert_condition_wmo_2">56 57 66 67 71 73 85 86</setting>
<setting id="alert_condition_wmo_3">75 95 96 99</setting>
```
Emphasizes freezing conditions and snow

**Commuter alerts:**
```xml
<setting id="alert_condition_wmo_1">45 48</setting>
<setting id="alert_condition_wmo_2">51 53 55 56 57 66 67 71 73 75</setting>
<setting id="alert_condition_wmo_3">82 95 96 99</setting>
```
Fog at notice (visibility), freezing conditions at caution, severe storms at danger

### Wind Speed Alerts

Wind speed alerts warn about sustained winds that may affect outdoor activities, travel, or cause property damage.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_windspeed_high_1/2/3` | Sustained wind speed thresholds |

#### Wind Speed Reference

| km/h | mph | Beaufort | Description | Effects |
|------|-----|----------|-------------|---------|
| <20 | <12 | 0-3 | Light | Calm to gentle breeze |
| 20-40 | 12-25 | 4-5 | Moderate | Small branches move |
| 40-60 | 25-38 | 6-7 | Strong | Large branches move, umbrellas difficult |
| 60-80 | 38-50 | 8-9 | Gale | Twigs break, walking difficult |
| 80-100 | 50-62 | 10 | Storm | Trees uprooted, structural damage |
| 100-120 | 62-75 | 11 | Violent storm | Widespread damage |
| >120 | >75 | 12 | Hurricane | Devastating damage |

#### Recommended Thresholds

| Environment | high_1 | high_2 | high_3 | Rationale |
|-------------|--------|--------|--------|-----------|
| Inland areas | 50 | 75 | 100 | Standard thresholds |
| Coastal areas | 60 | 90 | 120 | Higher baseline winds |
| Mountain areas | 70 | 100 | 130 | Adjusted for elevation |
| Urban areas | 40 | 60 | 80 | Buildings create wind tunnels |

### Wind Gust Alerts

Wind gusts are brief (few seconds) increases in wind speed that can be significantly higher than sustained winds. They often cause the most damage.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_windgust_high_1/2/3` | Wind gust speed thresholds |

#### Gusts vs. Sustained Wind

Gusts are typically 30-50% higher than sustained winds. A day with 60 km/h sustained winds might have gusts of 80-90 km/h.

**Gust impact reference:**
| km/h | Impact |
|------|--------|
| 60-80 | Difficult to walk, loose objects blown |
| 80-100 | Tree branches break, minor property damage |
| 100-130 | Large branches break, roof tiles lifted |
| 130+ | Trees uprooted, significant structural damage |

#### Recommended Thresholds

| Sensitivity | high_1 | high_2 | high_3 |
|-------------|--------|--------|--------|
| Conservative | 60 | 80 | 100 |
| Moderate | 70 | 90 | 120 |
| Minimal alerts | 80 | 100 | 130 |

### UV Index Alerts

The UV Index measures the strength of ultraviolet radiation from the sun. Higher values mean faster skin damage and higher cancer risk.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_uvindex_high_1/2/3` | UV Index thresholds |

#### UV Index Scale

| Index | Level | Time to Burn* | Recommended Protection |
|-------|-------|--------------|------------------------|
| 0-2 | Low | >60 min | Minimal needed |
| 3-5 | Moderate | 30-60 min | Hat, sunscreen |
| 6-7 | High | 15-30 min | Hat, sunscreen, shade |
| 8-10 | Very High | 10-15 min | Avoid midday sun |
| 11+ | Extreme | <10 min | Stay indoors if possible |

*For fair skin; darker skin types have more protection but still need care at high levels.

#### Recommended Thresholds

| Skin Type | high_1 | high_2 | high_3 |
|-----------|--------|--------|--------|
| Fair skin | 3 | 5 | 7 |
| Medium skin | 4 | 6 | 8 |
| Darker skin | 6 | 8 | 10 |
| General use | 5 | 7 | 9 |

### Humidity Alerts

Humidity alerts can warn about conditions that affect comfort, health, or property (mold risk).

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_humidity_high_1/2/3` | High humidity thresholds (%) |

**Note**: The addon may also support low humidity alerts for dry conditions.

#### Humidity Reference

| % | Comfort Level | Notes |
|---|---------------|-------|
| <30 | Too dry | Skin irritation, static electricity |
| 30-50 | Comfortable | Ideal indoor range |
| 50-60 | Slightly humid | Generally comfortable |
| 60-70 | Humid | Mold risk begins |
| 70-80 | Very humid | Uncomfortable, high mold risk |
| >80 | Oppressive | Health risk when combined with heat |

### Pressure Alerts

Atmospheric pressure alerts can indicate incoming weather systems. Rapidly falling pressure often precedes storms.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_pressure_high_1/2/3` | High pressure thresholds |
| `alert_pressuresurface_high_1/2/3` | Surface pressure thresholds |

#### Pressure Reference (hPa)

| Pressure | Typical Weather |
|----------|-----------------|
| >1030 | High pressure, clear skies |
| 1015-1030 | Normal conditions |
| 1000-1015 | Unsettled, possible rain |
| 980-1000 | Low pressure, storms likely |
| <980 | Very low, severe storms |

### Visibility Alerts

Visibility alerts warn about reduced visibility due to fog, mist, rain, snow, or other phenomena.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_visibility_low_1/2/3` | Visibility thresholds (in configured distance unit) |

**Note**: Visibility uses `low_` thresholds since lower values are more severe.

#### Visibility Reference

| Distance | Condition | Driving Impact |
|----------|-----------|----------------|
| >10 km | Clear | No impact |
| 4-10 km | Light haze | Minor |
| 1-4 km | Haze/mist | Reduce speed |
| 200m-1km | Fog | Significant, use fog lights |
| <200m | Dense fog | Dangerous, avoid driving |

### Feels Like Temperature Alerts

"Feels like" (apparent temperature) combines air temperature with wind chill or heat index to represent how weather actually feels to humans.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_feelslike_high_1/2/3` | High feels-like thresholds |
| `alert_feelslike_low_1/2/3` | Low feels-like thresholds |

#### When Feels-Like Differs from Actual Temperature

**Hot conditions** - Heat Index:
- 30°C with 70% humidity feels like 35°C
- 35°C with 50% humidity feels like 41°C

**Cold conditions** - Wind Chill:
- -5°C with 30 km/h wind feels like -12°C
- -10°C with 40 km/h wind feels like -21°C

### Dewpoint Alerts

Dewpoint indicates moisture content in the air and is a better indicator of humidity comfort than relative humidity.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_dewpoint_high_1/2/3` | Dewpoint thresholds |

#### Dewpoint Comfort Scale

| Dewpoint (°C) | Comfort Level |
|---------------|---------------|
| <10 | Dry, comfortable |
| 10-15 | Comfortable |
| 16-18 | Slightly humid |
| 18-21 | Humid, some discomfort |
| 21-24 | Very humid, uncomfortable |
| >24 | Oppressive, dangerous with heat |

### Cloudiness Alerts

Cloud cover alerts can be useful for astronomers, solar panel operators, or outdoor event planning.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_cloudiness_high_1/2/3` | Cloud cover thresholds (%) |

### Solar Radiation Alerts

Solar radiation (W/m²) is useful for solar energy production monitoring or photosensitivity concerns.

#### Settings

| Setting | Description |
|---------|-------------|
| `alert_solarradiation_high_1/2/3` | Solar radiation thresholds |

---

## Air Quality Alerts - Detailed Guide

Air quality monitoring is increasingly important for health, especially for vulnerable groups.

### Air Quality Index (AQI)

The addon supports both European (EU) and US AQI scales. Choose one based on your region.

#### European AQI (EAQI)

| Index | Level | Health Implications |
|-------|-------|---------------------|
| 0-20 | Good | Air quality is satisfactory |
| 20-40 | Fair | Acceptable, possible concern for very sensitive people |
| 40-60 | Moderate | Sensitive groups may experience effects |
| 60-80 | Poor | Health effects possible for everyone |
| 80-100 | Very Poor | Health alert, serious effects possible |
| >100 | Extremely Poor | Emergency conditions |

#### US AQI

| Index | Level | Health Implications |
|-------|-------|---------------------|
| 0-50 | Good | Air quality is satisfactory |
| 51-100 | Moderate | Acceptable, concern for unusually sensitive people |
| 101-150 | Unhealthy for Sensitive | Sensitive groups affected |
| 151-200 | Unhealthy | Everyone may experience effects |
| 201-300 | Very Unhealthy | Health warnings, everyone affected |
| >300 | Hazardous | Emergency conditions |

#### Recommended Thresholds

**EU AQI:**
| Sensitivity | high_1 | high_2 | high_3 |
|-------------|--------|--------|--------|
| Sensitive individual | 30 | 50 | 70 |
| General population | 40 | 60 | 80 |
| Less sensitive | 50 | 75 | 100 |

**US AQI:**
| Sensitivity | high_1 | high_2 | high_3 |
|-------------|--------|--------|--------|
| Sensitive individual | 50 | 100 | 150 |
| General population | 75 | 125 | 175 |
| Less sensitive | 100 | 150 | 200 |

### Particulate Matter (PM2.5 and PM10)

Particulate matter is classified by size:
- **PM2.5**: Fine particles <2.5 micrometers (most dangerous, penetrate lungs)
- **PM10**: Coarse particles <10 micrometers

#### PM2.5 Health Thresholds (μg/m³)

| Level | WHO Guideline | EU Limit | US Standard |
|-------|---------------|----------|-------------|
| Good | <5 | <10 | <12 |
| Moderate | 5-15 | 10-20 | 12-35 |
| Unhealthy | 15-25 | 20-25 | 35-55 |
| Very Unhealthy | 25-50 | 25-50 | 55-150 |
| Hazardous | >50 | >50 | >150 |

#### PM10 Health Thresholds (μg/m³)

| Level | WHO Guideline | EU Limit | US Standard |
|-------|---------------|----------|-------------|
| Good | <15 | <20 | <54 |
| Moderate | 15-45 | 20-40 | 54-154 |
| Unhealthy | 45-75 | 40-50 | 154-254 |
| Very Unhealthy | 75-100 | 50-100 | 254-354 |
| Hazardous | >100 | >100 | >354 |

### Other Pollutants

| Pollutant | Setting | Unit | Danger Threshold |
|-----------|---------|------|------------------|
| Ozone (O₃) | `alert_ozone` | μg/m³ | >180 (1-hour) |
| Nitrogen Dioxide (NO₂) | `alert_no2` | μg/m³ | >200 (1-hour) |
| Sulphur Dioxide (SO₂) | `alert_so2` | μg/m³ | >350 (1-hour) |
| Carbon Monoxide (CO) | `alert_co` | μg/m³ | >10000 (8-hour) |
| Dust | `alert_dust` | μg/m³ | Variable by region |

---

## Pollen Alerts - Detailed Guide

Pollen alerts are available for Europe only, using data from the Copernicus Atmosphere Monitoring Service.

### Available Pollen Types

| Pollen | Season (Europe) | Peak Months |
|--------|-----------------|-------------|
| Alder | Late winter/early spring | Feb-Mar |
| Birch | Spring | Mar-May |
| Grass | Late spring/summer | May-Jul |
| Mugwort | Late summer | Jul-Sep |
| Olive | Spring (Mediterranean) | Apr-Jun |
| Ragweed | Late summer/fall | Aug-Oct |

### Pollen Count Thresholds (grains/m³)

Thresholds vary by pollen type and individual sensitivity:

| Level | Birch | Grass | Ragweed | General |
|-------|-------|-------|---------|---------|
| Low | <10 | <20 | <5 | Minimal symptoms |
| Moderate | 10-50 | 20-50 | 5-20 | Mild symptoms |
| High | 50-200 | 50-150 | 20-100 | Significant symptoms |
| Very High | >200 | >150 | >100 | Severe symptoms |

### Configuring Pollen Alerts

Only enable alerts for pollens you're sensitive to:

```xml
<!-- Only enable birch and grass for spring allergies -->
<setting id="alert_birch_enabled">true</setting>
<setting id="alert_birch_danger">true</setting>
<setting id="alert_birch_high_3">100</setting>

<setting id="alert_grass_enabled">true</setting>
<setting id="alert_grass_danger">true</setting>
<setting id="alert_grass_high_3">75</setting>
```

---

## Alert Timing and Display Settings

### Timing Configuration

| Setting | Type | Range | Default | Description |
|---------|------|-------|---------|-------------|
| `alert_hours` | integer | 1-24 | 8 | Hours ahead to check for alerts |
| `alert_interval` | integer | 5-120 | 30 | Minutes between alert checks |
| `alert_duration` | integer | 5-60 | 15 | Seconds to display notification |

#### Choosing `alert_hours`

| Value | Use Case |
|-------|----------|
| 4 | Short-term, immediate concerns only |
| 8 | Good balance (default) - covers workday/commute |
| 12 | Half-day coverage, good for planning |
| 24 | Full day ahead warning |

**Consideration**: Longer windows catch more events but may feel less urgent. A thunderstorm alert 20 hours ahead is less actionable than 4 hours ahead.

#### Choosing `alert_interval`

| Value | Use Case |
|-------|----------|
| 10-15 | Rapidly changing weather, severe weather season |
| 30 | Normal use (default) |
| 60 | Stable weather periods, reduce system load |

### Display Colors

Customize the colors used in alert displays:

| Setting | Default | Description |
|---------|---------|-------------|
| `colordefault` | lightgrey | Inactive/neutral state |
| `colornegative` | deepskyblue | Negative values (e.g., below-zero temps) |
| `colornormal` | forestgreen | Normal/good conditions |
| `colornotice` | yellow | Notice level alerts |
| `colorcaution` | orange | Caution level alerts |
| `colordanger` | crimson | Danger level alerts |

Colors can be specified as:
- Named colors: `red`, `blue`, `orange`, `crimson`, etc.
- Hex codes: `#FF5500` or `FF5500`

---

## WMO Weather Code Complete Reference

The World Meteorological Organization (WMO) defines standardized codes for weather conditions. The Open-Meteo addon uses these codes for condition-based alerts.

### Code 0-3: Clear and Cloudy

| Code | Condition | Day Icon | Night Icon |
|------|-----------|----------|------------|
| 0 | Clear sky | Sunny | Clear |
| 1 | Mainly clear | Mainly Sunny | Mainly Clear |
| 2 | Partly cloudy | Partly Cloudy | Partly Cloudy |
| 3 | Overcast | Cloudy | Cloudy |

**Alert recommendation**: Generally not alertable conditions

### Code 45-48: Fog

| Code | Condition | Visibility | Risk Level |
|------|-----------|------------|------------|
| 45 | Fog | Reduced | Moderate |
| 48 | Depositing rime fog | Reduced + ice | Elevated |

**Alert recommendation**: Notice or Caution for drivers
- Rime fog (48) is more hazardous due to ice formation on surfaces

### Code 51-57: Drizzle

| Code | Condition | Intensity | Hourly mm |
|------|-----------|-----------|-----------|
| 51 | Light drizzle | Light | <0.25 |
| 53 | Moderate drizzle | Moderate | 0.25-1 |
| 55 | Dense drizzle | Heavy | >1 |
| 56 | Light freezing drizzle | Light + ice | <0.25 |
| 57 | Dense freezing drizzle | Heavy + ice | >0.25 |

**Alert recommendation**:
- 51: Notice (may need umbrella)
- 53: Notice or Caution
- 55: Caution (persistent wet conditions)
- 56-57: Caution to Danger (ice hazard)

### Code 61-67: Rain

| Code | Condition | Intensity | Hourly mm |
|------|-----------|-----------|-----------|
| 61 | Slight rain | Light | <2.5 |
| 63 | Moderate rain | Moderate | 2.5-7.5 |
| 65 | Heavy rain | Heavy | >7.5 |
| 66 | Light freezing rain | Light + ice | <2.5 |
| 67 | Heavy freezing rain | Heavy + ice | >2.5 |

**Alert recommendation**:
- 61: Notice
- 63: Caution
- 65: Caution to Danger
- 66: Caution (ice forming)
- 67: Danger (significant ice accumulation)

### Code 71-77: Snow

| Code | Condition | Intensity | Hourly cm |
|------|-----------|-----------|-----------|
| 71 | Slight snow | Light | <1 |
| 73 | Moderate snow | Moderate | 1-4 |
| 75 | Heavy snow | Heavy | >4 |
| 77 | Snow grains | Light | Trace |

**Alert recommendation**:
- 71, 77: Notice (travel caution)
- 73: Caution (accumulation likely)
- 75: Danger (significant accumulation, travel dangerous)

### Code 80-86: Showers

| Code | Condition | Intensity | Description |
|------|-----------|-----------|-------------|
| 80 | Slight rain showers | Light | Brief, light |
| 81 | Moderate rain showers | Moderate | Intermittent |
| 82 | Violent rain showers | Heavy | Intense, flash flooding |
| 85 | Slight snow showers | Light | Brief snow |
| 86 | Heavy snow showers | Heavy | Intense snow bursts |

**Alert recommendation**:
- 80, 85: Notice
- 81: Caution
- 82: Danger (flash flood risk)
- 86: Danger (sudden accumulation)

### Code 95-99: Thunderstorms

| Code | Condition | Hazards |
|------|-----------|---------|
| 95 | Thunderstorm | Lightning, heavy rain, gusty winds |
| 96 | Thunderstorm with slight hail | Above + small hail |
| 99 | Thunderstorm with heavy hail | Above + large, damaging hail |

**Alert recommendation**: All should be Danger level
- Lightning kills, hail damages property and vehicles
- Always seek shelter during thunderstorms

### Quick Reference by Severity

**Low severity (Notice candidates):**
```
45 48 51 56 61 66 71 77 80 85
```

**Medium severity (Caution candidates):**
```
53 55 57 63 67 73 81 86
```

**High severity (Danger candidates):**
```
65 75 82 95 96 99
```

---

## Regional Threshold Recommendations

### Northwestern Europe (UK, Netherlands, Belgium, Northern France, Northern Germany)

**Climate characteristics**: Maritime, mild winters, cool summers, frequent rain, occasional storms

```xml
<!-- Temperature: Mild climate, extremes are notable -->
<setting id="alert_temperature_high_1">28</setting>
<setting id="alert_temperature_high_2">32</setting>
<setting id="alert_temperature_high_3">36</setting>
<setting id="alert_temperature_low_1">-3</setting>
<setting id="alert_temperature_low_2">-8</setting>
<setting id="alert_temperature_low_3">-15</setting>

<!-- Precipitation: Regular rain, but heavy events notable -->
<setting id="alert_precipitation_high_1">15</setting>
<setting id="alert_precipitation_high_2">30</setting>
<setting id="alert_precipitation_high_3">50</setting>

<!-- Wind: Coastal influences -->
<setting id="alert_windspeed_high_1">50</setting>
<setting id="alert_windspeed_high_2">75</setting>
<setting id="alert_windspeed_high_3">100</setting>

<setting id="alert_windgust_high_1">70</setting>
<setting id="alert_windgust_high_2">90</setting>
<setting id="alert_windgust_high_3">120</setting>

<!-- Conditions: Include freezing rain for rare but impactful events -->
<setting id="alert_condition_wmo_3">67 75 82 95 96 99</setting>
```

### Mediterranean (Southern France, Spain, Italy, Greece)

**Climate characteristics**: Hot dry summers, mild wet winters, occasional severe storms

```xml
<!-- Temperature: Higher heat thresholds -->
<setting id="alert_temperature_high_1">33</setting>
<setting id="alert_temperature_high_2">38</setting>
<setting id="alert_temperature_high_3">42</setting>
<setting id="alert_temperature_low_1">0</setting>
<setting id="alert_temperature_low_2">-5</setting>
<setting id="alert_temperature_low_3">-10</setting>

<!-- Precipitation: Often intense when it comes -->
<setting id="alert_precipitation_high_1">20</setting>
<setting id="alert_precipitation_high_2">40</setting>
<setting id="alert_precipitation_high_3">70</setting>

<!-- Wind: Mistral, Sirocco possible -->
<setting id="alert_windspeed_high_1">60</setting>
<setting id="alert_windspeed_high_2">90</setting>
<setting id="alert_windspeed_high_3">120</setting>
```

### Nordic Countries (Norway, Sweden, Finland, Denmark)

**Climate characteristics**: Cold winters, mild summers, snow common

```xml
<!-- Temperature: Adjusted for cold climate -->
<setting id="alert_temperature_high_1">25</setting>
<setting id="alert_temperature_high_2">28</setting>
<setting id="alert_temperature_high_3">32</setting>
<setting id="alert_temperature_low_1">-15</setting>
<setting id="alert_temperature_low_2">-25</setting>
<setting id="alert_temperature_low_3">-35</setting>

<!-- Snow is routine; raise thresholds -->
<setting id="alert_condition_wmo_2">73</setting>
<setting id="alert_condition_wmo_3">75 82 95 96 99</setting>
```

### Central Europe (Germany, Austria, Switzerland, Czech Republic, Poland)

**Climate characteristics**: Continental, warm summers, cold winters, four distinct seasons

```xml
<!-- Temperature: Full range -->
<setting id="alert_temperature_high_1">30</setting>
<setting id="alert_temperature_high_2">35</setting>
<setting id="alert_temperature_high_3">38</setting>
<setting id="alert_temperature_low_1">-10</setting>
<setting id="alert_temperature_low_2">-18</setting>
<setting id="alert_temperature_low_3">-25</setting>

<!-- Summer storms can be severe -->
<setting id="alert_windgust_high_3">130</setting>
```

### North American East Coast

**Climate characteristics**: Hot humid summers, cold winters, nor'easters, hurricanes (south)

```xml
<!-- Temperature: Wide range -->
<setting id="alert_temperature_high_1">32</setting>
<setting id="alert_temperature_high_2">35</setting>
<setting id="alert_temperature_high_3">40</setting>
<setting id="alert_temperature_low_1">-10</setting>
<setting id="alert_temperature_low_2">-20</setting>
<setting id="alert_temperature_low_3">-30</setting>

<!-- Hurricane/Nor'easter wind thresholds -->
<setting id="alert_windspeed_high_3">120</setting>
<setting id="alert_windgust_high_3">160</setting>

<!-- Heavy precipitation events -->
<setting id="alert_precipitation_high_3">75</setting>
```

---

## Use Case Examples

### Example 1: "Alert Me Only for Dangerous Weather"

User wants minimal notifications, only for truly severe conditions:

```xml
<!-- Enable only danger level for all alert types -->
<setting id="alert_temperature_notice">false</setting>
<setting id="alert_temperature_caution">false</setting>
<setting id="alert_temperature_danger">true</setting>

<!-- High thresholds -->
<setting id="alert_temperature_high_3">38</setting>
<setting id="alert_temperature_low_3">-20</setting>
<setting id="alert_precipitation_high_3">50</setting>
<setting id="alert_windgust_high_3">130</setting>

<!-- Only severe conditions -->
<setting id="alert_condition_wmo_1"></setting>
<setting id="alert_condition_wmo_2"></setting>
<setting id="alert_condition_wmo_3">75 82 95 96 99</setting>

<!-- Disable non-critical alerts -->
<setting id="alert_uvindex_enabled">false</setting>
<setting id="alert_humidity_enabled">false</setting>
<setting id="alert_cloudiness_enabled">false</setting>
```

### Example 2: "Daily Commuter Alerts"

User drives to work and wants advance warning of conditions affecting the commute:

```xml
<!-- Check 4 hours ahead (enough for commute planning) -->
<setting id="alert_hours">4</setting>

<!-- Enable notice and above for visibility/road conditions -->
<setting id="alert_condition_notice">true</setting>
<setting id="alert_condition_caution">true</setting>
<setting id="alert_condition_danger">true</setting>

<!-- Fog is important for drivers -->
<setting id="alert_condition_wmo_1">45 48 51 61 71 80</setting>
<setting id="alert_condition_wmo_2">53 56 57 63 66 67 73 81 85</setting>
<setting id="alert_condition_wmo_3">55 65 75 82 86 95 96 99</setting>

<!-- Visibility alerts -->
<setting id="alert_visibility_enabled">true</setting>
<setting id="alert_visibility_notice">true</setting>
<setting id="alert_visibility_low_1">4000</setting>
<setting id="alert_visibility_low_2">1000</setting>
<setting id="alert_visibility_low_3">200</setting>

<!-- Wind gusts affect vehicle handling -->
<setting id="alert_windgust_notice">true</setting>
<setting id="alert_windgust_high_1">60</setting>
```

### Example 3: "Outdoor Enthusiast/Hiker"

User spends weekends hiking and needs comprehensive weather awareness:

```xml
<!-- Full day ahead planning -->
<setting id="alert_hours">12</setting>

<!-- All alert levels for outdoor safety -->
<setting id="alert_temperature_notice">true</setting>
<setting id="alert_temperature_caution">true</setting>
<setting id="alert_temperature_danger">true</setting>

<!-- UV protection important -->
<setting id="alert_uvindex_enabled">true</setting>
<setting id="alert_uvindex_notice">true</setting>
<setting id="alert_uvindex_high_1">5</setting>
<setting id="alert_uvindex_high_2">7</setting>
<setting id="alert_uvindex_high_3">9</setting>

<!-- Thunderstorms are dangerous outdoors -->
<setting id="alert_condition_notice">true</setting>
<setting id="alert_condition_wmo_1">80 85</setting>
<setting id="alert_condition_wmo_2">63 73 81 86</setting>
<setting id="alert_condition_wmo_3">65 75 82 95 96 99</setting>

<!-- Wind affects hiking safety -->
<setting id="alert_windgust_notice">true</setting>
<setting id="alert_windgust_high_1">50</setting>
<setting id="alert_windgust_high_2">70</setting>
<setting id="alert_windgust_high_3">90</setting>
```

### Example 4: "Allergy Sufferer"

User has severe pollen allergies and needs advance warning:

```xml
<!-- Enable relevant pollen alerts -->
<setting id="alert_birch_enabled">true</setting>
<setting id="alert_birch_notice">true</setting>
<setting id="alert_birch_caution">true</setting>
<setting id="alert_birch_danger">true</setting>
<setting id="alert_birch_high_1">20</setting>
<setting id="alert_birch_high_2">50</setting>
<setting id="alert_birch_high_3">100</setting>

<setting id="alert_grass_enabled">true</setting>
<setting id="alert_grass_notice">true</setting>
<setting id="alert_grass_caution">true</setting>
<setting id="alert_grass_danger">true</setting>
<setting id="alert_grass_high_1">15</setting>
<setting id="alert_grass_high_2">40</setting>
<setting id="alert_grass_high_3">80</setting>

<!-- Also monitor air quality -->
<setting id="alert_aqieu_enabled">true</setting>
<setting id="alert_aqieu_notice">true</setting>
<setting id="alert_aqieu_high_1">30</setting>
<setting id="alert_aqieu_high_2">50</setting>
<setting id="alert_aqieu_high_3">70</setting>
```

### Example 5: "Home Automation Integration"

User wants alerts that trigger home automation actions:

```xml
<!-- Longer alert display for automation processing -->
<setting id="alert_duration">30</setting>

<!-- Check more frequently -->
<setting id="alert_interval">15</setting>

<!-- Enable all levels for granular automation triggers -->
<setting id="alert_temperature_notice">true</setting>
<setting id="alert_temperature_caution">true</setting>
<setting id="alert_temperature_danger">true</setting>

<!-- Tighter thresholds for HVAC optimization -->
<setting id="alert_temperature_high_1">24</setting>
<setting id="alert_temperature_high_2">27</setting>
<setting id="alert_temperature_high_3">30</setting>
<setting id="alert_temperature_low_1">5</setting>
<setting id="alert_temperature_low_2">0</setting>
<setting id="alert_temperature_low_3">-5</setting>

<!-- Solar radiation for blinds/shades -->
<setting id="alert_solarradiation_enabled">true</setting>
<setting id="alert_solarradiation_notice">true</setting>
<setting id="alert_solarradiation_high_1">400</setting>
<setting id="alert_solarradiation_high_2">700</setting>
<setting id="alert_solarradiation_high_3">900</setting>
```

---

## Troubleshooting

### Alerts Not Appearing

1. **Check master enable**: Ensure `alert_[TYPE]_enabled` is `true`
2. **Check level enables**: At least one of `_notice`, `_caution`, `_danger` must be `true`
3. **Check thresholds**: Verify values are appropriate for your units and region
4. **Check location alerts**: Ensure `loc[N]alert` is `true` for your location
5. **Check Kodi notifications**: Ensure Kodi's notification system is enabled

### Too Many Alerts

1. **Disable lower severity levels**: Set `_notice` and `_caution` to `false`
2. **Raise thresholds**: Increase `_high_3` values
3. **Reduce condition codes**: Remove less severe WMO codes from your lists
4. **Increase alert_hours**: Shorter windows catch fewer events
5. **Disable non-essential alerts**: Turn off humidity, cloudiness, etc.

### Wrong Units in Alerts

1. **Check unit settings**: Verify `unittemp`, `unitspeed`, `unitprecip` etc.
2. **Adjust thresholds**: Thresholds must be in your configured units
3. **Recalculate after unit change**: If you change units, recalculate all thresholds

### Alerts Not Matching Actual Weather

1. **Check coordinates**: Verify `loc[N]lat` and `loc[N]lon` are correct
2. **Weather models**: Open-Meteo combines models; local variations possible
3. **Timing**: Alerts are based on forecasts, which aren't perfect
4. **Threshold calibration**: Adjust thresholds based on your observations

### Settings Reset After Update

1. **Backup settings.xml**: Before addon updates
2. **Restore after update**: Copy your backed-up settings.xml back
3. **Check for new settings**: New versions may add settings with defaults

### Performance Issues

1. **Increase alert_interval**: Check less frequently (e.g., 60 minutes)
2. **Disable unused alerts**: Turn off alerts you don't need
3. **Reduce map layers**: Disable unused map types
4. **Lower map history**: Reduce `maphistory` value

---

## Advanced Configuration

### Editing Settings Directly

1. **Locate the file**: See [File Locations](#file-locations)
2. **Stop Kodi**: Changes while running may be overwritten
3. **Edit carefully**: Maintain XML structure
4. **Validate**: Ensure all tags are properly closed
5. **Restart Kodi**: Load new settings

### Backing Up Settings

**Linux/Mac:**
```bash
cp ~/.kodi/userdata/addon_data/weather.openmeteo/settings.xml ~/weather-backup.xml
```

**Windows (PowerShell):**
```powershell
Copy-Item "$env:APPDATA\Kodi\userdata\addon_data\weather.openmeteo\settings.xml" -Destination "C:\backup\weather-backup.xml"
```

### Migrating Settings Between Devices

1. Export settings.xml from source device
2. Copy to same path on destination device
3. Restart Kodi on destination device

### Using Multiple Configurations

You can maintain multiple settings files for different scenarios:

```bash
# Backup current settings
cp settings.xml settings-summer.xml

# Swap to winter configuration
cp settings-winter.xml settings.xml

# Restart Kodi to load
```

### Integration with Skins

The addon exposes numerous window properties that skins can use:

```
Window(weather).Property(current.[property])
Window(weather).Property(hourly.[N].[property])
Window(weather).Property(daily.[N].[property])
Window(weather).Property(alert.[type])
Window(weather).Property(alert.[type].name)
Window(weather).Property(alert.[type].value)
Window(weather).Property(alert.[type].icon)
```

Alert values:
- 0 = No alert
- 1 = Notice
- 2 = Caution
- 3 = Danger

Skin developers can use these to display custom alert visualizations.

---

## Frequently Asked Questions

### General Questions

**Q: Does the addon require an API key?**
A: No, Open-Meteo provides free access without registration for non-commercial use.

**Q: How accurate are the forecasts?**
A: Open-Meteo combines multiple national weather service models. Accuracy is comparable to major weather services, typically best for 1-3 days ahead.

**Q: How often is data updated?**
A: Weather data is refreshed approximately every 30 minutes. You can configure refresh interval via `alert_interval`.

**Q: Does it work offline?**
A: The addon requires internet access to fetch weather data. Cached data may be displayed briefly if connectivity is lost.

### Alert Questions

**Q: Why am I getting alerts for mild conditions?**
A: Your thresholds may be too low. Review the regional recommendations and adjust `_high_1/2/3` values upward.

**Q: Can I have different thresholds for different locations?**
A: Currently, thresholds are global. You can only enable/disable alerts per location via `loc[N]alert`.

**Q: What's the difference between wind speed and wind gust alerts?**
A: Wind speed is the sustained (average) wind. Gusts are brief peaks that can be 30-50% higher and often cause more damage.

**Q: How do precipitation alerts handle snow vs. rain?**
A: Precipitation is measured as liquid water equivalent. Snow is converted (roughly 10cm snow = 1cm rain/10mm).

### Technical Questions

**Q: Where are the weather maps stored?**
A: In Kodi's addon_data folder under `weather.openmeteo/cache/`

**Q: Can I reduce bandwidth usage?**
A: Yes - increase `alert_interval`, disable unused map layers, reduce `maphistory`

**Q: The addon seems slow, what can I do?**
A: Increase `alert_interval`, reduce enabled alert types, disable maps you don't use

**Q: How do I report a bug?**
A: Visit the GitHub issues page: https://github.com/bkury/weather.openmeteo/issues

---

## File Locations

### Settings File Location by Platform

| Platform | Path |
|----------|------|
| **Windows** | `%APPDATA%\Kodi\userdata\addon_data\weather.openmeteo\settings.xml` |
| **Linux** | `~/.kodi/userdata/addon_data/weather.openmeteo/settings.xml` |
| **LibreELEC/CoreELEC** | `/storage/.kodi/userdata/addon_data/weather.openmeteo/settings.xml` |
| **OSMC** | `/home/osmc/.kodi/userdata/addon_data/weather.openmeteo/settings.xml` |
| **macOS** | `~/Library/Application Support/Kodi/userdata/addon_data/weather.openmeteo/settings.xml` |
| **Android** | `/sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/addon_data/weather.openmeteo/settings.xml` |
| **iOS** | `/private/var/mobile/Library/Preferences/Kodi/userdata/addon_data/weather.openmeteo/settings.xml` |
| **Portable Install** | `[Kodi folder]\portable_data\userdata\addon_data\weather.openmeteo\settings.xml` |

### Cache Location

Weather data cache and map images are stored in:
```
[addon_data path]/weather.openmeteo/cache/
```

### Log File Location

Debug information is written to:
```
[kodi userdata]/kodi.log
```

Enable debug logging with:
```xml
<setting id="debug">true</setting>
<setting id="verbose">true</setting>
```

---

## Credits and Data Sources

### Addon Development

- **Author**: bkury
- **Repository**: https://github.com/bkury/weather.openmeteo
- **License**: GPL-2.0

### Weather Data Providers

| Provider | Data | Coverage |
|----------|------|----------|
| **Open-Meteo** | Weather forecasts, air quality | Global |
| **RainViewer** | Precipitation radar, satellite | Global |
| **weather.gc.ca** | Temperature/wind maps | Global |
| **met.no** | Weather data | Global |
| **Copernicus CAMS** | Pollen data | Europe |

### Standards

- **WMO**: World Meteorological Organization weather codes
- **EAQI**: European Air Quality Index
- **US AQI**: United States Air Quality Index

### Translations

The addon is translated via Weblate with contributions from the community:
https://hosted.weblate.org/projects/openht/weather-openmeteo/

---

## Document Information

- **Version**: 1.0
- **Last Updated**: December 2024
- **Addon Version**: 1.0.29
- **Kodi Compatibility**: 21 (Omega) and later