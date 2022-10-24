"""Constants for Chargesplit."""
# Base component constants
NAME = "Chargesplit Domus"
DOMAIN = "Chargesplit"
VERSION = "0.0.1"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_CODE = "code"
CONF_SYNC_INTERVAL = "sync_interval"
CHARGEPOINT_SERIAL =  "serial"
DEFAULT_SYNC_INTERVAL = 60  # seconds

CONF_MAX_CHARGING_CURRENT_KEY = "PILOTLIMIT"