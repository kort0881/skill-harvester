---
name: "weather-plugin"
description: "Guide for using the weather plugin — data queries, radar imagery, model maps, and meteorological calculations"
---

# Weather Plugin Usage Guide

You have access to **12 weather tools**. Prefer lightweight data tools and only request images when explicitly asked.

## Tool List

| Tool | Purpose |
|------|---------|
| `wx_conditions` | Current conditions for a location |
| `wx_forecast`   | Textual forecast summary |
| `wx_alerts`     | Active weather alerts/watches |
| `wx_metar`      | Raw METAR report |
| `wx_brief`      | Combined conditions, forecast, and alerts |
| `wx_global`     | Worldwide conditions (non‑US) |
| `wx_severe`     | Severe weather outlook |
| `wx_radar_image`| NEXRAD radar PNG image |
| `wx_model_image`| Model‑derived PNG images (e.g., CAPE, helicity) |
| `wx_storm_image`| Storm‑scale imagery |
| `wx_calc`       | Meteorological calculations (dewpoint, wind chill, etc.) |
| `wx_sounding`   | Atmospheric sounding data |

**Do NOT call any other tool names.**

## Common Query Mappings

- "How's the weather in **[place]**?" → `wx_conditions`
- "What's the forecast?" → `wx_forecast`
- "Any warnings/watches?" → `wx_alerts`
- "Show me the radar" → `wx_radar_image`
- "Show me CAPE/temperature/wind map" → `wx_model_image` (comma‑separated vars, e.g., `"cape,helicity,uh,srh"`)
- "What's the severe weather outlook?" → `wx_severe`
- "Weather in Tokyo/London/etc" → `wx_global`
- "Calculate dewpoint/wind chill/LCL" → `wx_calc`
- "Is there a tornado threat?" → `wx_severe` then `wx_model_image --var cape` or `--var helicity`
- "What does the HRRR show?" → `wx_model_image` with appropriate variable
- "Show me the 18z HRRR" → `wx_model_image` with `cycle: 18`
- "Sounding at a point" → `wx_sounding`

## Operational Rules

1. **Start lightweight.** Use `wx_conditions` or `wx_brief` before heavier tools.
2. **Images only on request.** Do not invoke `wx_radar_image` or `wx_model_image` unless the user explicitly wants to see an image.
3. **US vs International.** Use `wx_global` for non‑US locations; otherwise prefer US‑specific tools.
4. **Verified calculations.** `wx_calc` relies on Rust‑backed functions verified against MetPy.
5. **Avoid redundancy.** `wx_brief` already includes conditions, forecast, and alerts; do not call those three separately after it.
6. **Batch model images.** Never call `wx_model_image` multiple times for different variables. Use a single call with a comma‑separated list (e.g., `"cape,helicity,uh,srh"`).
7. **Severe‑weather package.** For a full severe analysis, request `wx_model_image` with `var: "cape,helicity,uh,srh"` to obtain four images in one call.
8. **Zoom to region.** When the user specifies a corridor or region, always provide `lat`, `lon`, and `radius_km` to limit the image extent. Example mappings:
   - "Ohio Valley" → `lat: 39.5, lon: -83, radius_km: 400`
   - "Indiana to New York" → `lat: 40.5, lon: -77, radius_km: 500`
   - "Texas" → `lat: 31.5, lon: -99, radius_km: 500`
   - "Southeast" → `lat: 33, lon: -85, radius_km: 600`
   - "Great Plains" → `lat: 38, lon: -99, radius_km: 600`

## `wx_calc` Example Payloads

```json
{ "function": "dewpoint_from_relative_humidity", "args": { "temperature": "30 degC", "relative_humidity": "65 percent" } }
```
```json
{ "function": "wind_chill", "args": { "temperature": "-5 degC", "speed": "30 km/hr" } }
```
```json
{ "function": "heat_index", "args": { "temperature": "95 degF", "relative_humidity": "60 percent" } }
```
```json
{ "function": "lcl", "args": { "pressure": "1000 hPa", "temperature": "30 degC", "dewpoint": "20 degC" } }
```

## Image Tools Details

- **`wx_radar_image`** returns a JSON object with a PNG file path. Provide a NEXRAD site ID (e.g., `KRTX` for Portland, `KTLX` for Oklahoma City, `KLOT` for Chicago) **or** latitude/longitude. Default size is 1024 px, range 200 km, with a 10 dBZ noise filter.
- **`wx_model_image`** returns PNG paths for the requested variables. Supported variables include `cape, refl, temp, dewpoint, rh, gust, helicity, uh, precip, mslp, heights_500, jet, srh`. Include `lat`, `lon`, and `radius_km` to zoom, and optionally a `cycle` parameter for specific model run times.

---
