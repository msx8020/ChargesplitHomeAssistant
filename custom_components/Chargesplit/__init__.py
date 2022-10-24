import logging

import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.const import  Platform

from .api import ChargesplitApi
from .const import (
    CONF_CODE,
    CHARGEPOINT_SERIAL,
    CONF_SYNC_INTERVAL,
    DEFAULT_SYNC_INTERVAL,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import ChargesplitDataUpdateCoordinator

PLATFORMS = [Platform.SENSOR, Platform.SELECT]

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    code = entry.data.get(CONF_CODE)
    serial = entry.data.get(CHARGEPOINT_SERIAL)
    api = ChargesplitApi(code,serial)
    sync_interval = DEFAULT_SYNC_INTERVAL #entry.options.get(CONF_SYNC_INTERVAL, DEFAULT_SYNC_INTERVAL)
    _LOGGER.warning(serial)
    coordinator = ChargesplitDataUpdateCoordinator(
        hass, api=api, update_interval=sync_interval
    )
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN] = coordinator
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = hass.data[DOMAIN]
    unloaded = all(
        await asyncio.gather(
            [
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN] = []

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
