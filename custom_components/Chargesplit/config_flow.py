import logging

import voluptuous as vol
import traceback

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import ChargesplitApi
from .const import (
    CONF_CODE,
    CHARGEPOINT_SERIAL,
    CONF_SYNC_INTERVAL,
    DEFAULT_SYNC_INTERVAL,
    DOMAIN,
    PLATFORMS,
)

_LOGGER = logging.getLogger(__name__)


class ChargesplitFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        self._errors = {}

    async def async_step_user(self, user_input=None):
        self._errors = {}


        if user_input is not None:
            valid = await self._test_credentials(
            user_input[CONF_CODE],user_input[CHARGEPOINT_SERIAL]
            )
            if valid:
                return self.async_create_entry(
                    title=user_input[CHARGEPOINT_SERIAL], data=user_input
                )
            else:
                self._errors["base"] = "auth"

            return await self._show_config_form(user_input)

        return await self._show_config_form(user_input)
        


    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CHARGEPOINT_SERIAL): str,vol.Required(CONF_CODE): str}
            ),
            errors=self._errors,
        )

    async def _test_credentials(self,code, serial):
        try:
            api = ChargesplitApi(code, serial)
            await self.hass.async_add_executor_job(api.test_auth)
            return True
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.error(
                f"{DOMAIN} Exception in login : %s - traceback: %s",
                ex,
                traceback.format_exc(),
            )
        return False

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ChargesplitOptionsFlowHandler(config_entry)

class ChargesplitOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        return await self.async_step_user()

        await self.async_set_unique_id(device_unique_id)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_SYNC_INTERVAL), data=self.options
        )

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()


        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                
                    vol.Required(
                        CONF_SYNC_INTERVAL,
                        default=self.options.get(
                            CONF_SYNC_INTERVAL, DEFAULT_SYNC_INTERVAL
                        ),
                    ): vol.All(vol.Coerce(int))
                
                }
            ),
        )

    
    async def _update_options(self):


        self.options = {'sync_interval': 60}
        return self.async_create_entry(
        title=self.config_entry.data.get(CONF_SYNC_INTERVAL), data=self.options
        )
