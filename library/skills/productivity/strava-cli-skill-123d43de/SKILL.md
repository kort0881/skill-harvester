---
name: "strava"
description: "Query and manage Strava fitness data via the `strava` CLI, including activities, athlete stats, segments, routes, clubs, and gear."
---

# Strava CLI Skill

## Prerequisites

- **Install the CLI**:
  ```bash
  curl -fsSL https://raw.githubusercontent.com/eddmann/strava-cli/main/install.sh | sh
  ```
- **Authenticate** (requires your own `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET`):
  ```bash
  strava auth login
  ```

## Quick Context

Retrieve an aggregated view of your athlete profile:

```bash
strava context                          # Full context: athlete, stats, gear, clubs, activities
strava context --activities 10          # Most recent 10 activities
strava context --focus stats,gear       # Only stats and gear sections
```

## Commands Overview

Run `strava --help` or `strava <command> --help` for detailed options.

### Activities
```bash
strava activities list [--after DATE] [--before DATE] [--limit N]
strava activities get <ID>
strava activities streams <ID> [--keys time,distance,heartrate,watts]
strava activities laps <ID>
strava activities zones <ID>
strava activities comments <ID>
strava activities kudos <ID>
```

### Athlete
```bash
strava athlete                # Profile summary
strava athlete stats          # Year‑to‑date and all‑time totals
strava athlete zones          # Heart‑rate / power zones
```

### Segments & Efforts
```bash
strava segments get <ID>
strava segments starred
strava segments explore --bounds SW_LAT,SW_LNG,NE_LAT,NE_LNG
strava efforts get <ID>
strava efforts list --segment-id <ID>
```

### Routes, Clubs, Gear
```bash
strava routes list
strava routes get <ID>
strava routes streams <ID>
strava routes export <ID> --format gpx|tcx
strava clubs list
strava clubs get <ID>
strava clubs members <ID> [--limit N]
strava clubs activities <ID> [--limit N]
strava gear get <GEAR_ID>
```

## Data Units
| Field                     | Unit    |
|---------------------------|---------|
| distance                  | meters  |
| moving_time, elapsed_time | seconds |
| average_speed, max_speed | m/s     |
| elevation                 | meters  |
| dates                     | ISO8601 |

## Common Patterns
```bash
# Recent activities (default limit 30)
strava activities list --limit 10

# Activities for the current month
strava activities list --after 2025-12-01

# Filter runs with jq
strava activities list | jq '[.[] | select(.sport_type=="Run")]'

# Compute total distance
strava activities list | jq '[.[].distance] | add'
```

## Authentication Status
```bash
strava auth status    # Show current auth state
strava auth refresh   # Refresh the access token
strava auth logout    # Remove stored credentials
```

## Sport Types
Run, TrailRun, Walk, Hike, Ride, MountainBikeRide, GravelRide, EBikeRide, VirtualRide, VirtualRun, Swim, Workout, WeightTraining, Yoga, CrossFit, Rowing, Kayaking, Surf, Ski, Snowboard, IceSkate, Golf, Soccer, Tennis

## Exit Codes
- `0` – Success
- `1` – General error
- `2` – Authentication error (run `strava auth login`)
