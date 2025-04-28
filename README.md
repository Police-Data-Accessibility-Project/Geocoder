# Geocoder
Geocodes locations for the Data Sources App


# Installation

- Install pipx

```bash
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

- Install `uv` using pipx

```bash
pipx install uv
```

- Create and activate a virtual environment

```bash
uv venv .venv
source .venv/bin/activate
```

- Sync dependencies

```bash
uv sync
```

# Environment Variables

```dotenv
DISCORD_WEBHOOK_URL=    # Discord webhook URL, for posting to Discord
PDAP_EMAIL=             # Email for PDAP login
PDAP_PASSWORD=          # Password for PDAP login
PDAP_API_URL=           # Optional, for if using non-default PDAP URL
LOCATION_IQ_API_KEY=    # LocationIQ API key, from https://my.locationiq.com/dashboard#accesstoken
```

