import logging

import asyncio
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

from .const import CONF_CODE, CONF_ENABLED, DOMAIN, PLATFORMS,CHARGEPOINT_SERIAL
from .api import ChargesplitApi

_LOGGER: logging.Logger = logging.getLogger(__package__)


class ChargesplitDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(
        self, hass: HomeAssistant, api: ChargesplitApi, update_interval: int
    ) -> None:
        self.api = api
        self.platforms = []

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self):
        try:
            return await self.hass.async_add_executor_job(self.api.get_data)
        except Exception as exception:
            raise UpdateFailed() from exception
