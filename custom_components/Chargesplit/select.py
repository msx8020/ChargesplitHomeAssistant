
import logging
import requests
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, NAME, VERSION

_LOGGER = logging.getLogger(__name__)


CHARGEPOINT_OPERATION_MODES = [
    "6", "7", "8", "9", "10", "11", "12", "13", "14", "15",
    "16", "17", "18", "19", "20", "21", "22", "23", "24", "25",
    "26", "27", "28", "29", "30", "31", "32",
]

CHARGEPOINT_LOCK_MODES = [
    "LOCK",
    "UNLOCK",
]

CHARGEPOINT_PAUSE_MODES = [
    "PAUSE",
    "RESTART",
]


OPERATION_MODE = SelectEntityDescription(
    key="operation_mode",
    name="Select Chargepoint Power AMPS",
    icon="mdi:ev-charger",
    entity_category=EntityCategory.CONFIG,
)

LOCK_MODE = SelectEntityDescription(
    key="lock_mode",
    name="Send Lock/unlock command",
    icon="mdi:ev-charger",
    entity_category=EntityCategory.CONFIG,
)

PAUSE_MODE = SelectEntityDescription(
    key="pause_mode",
    name="Send pause/restart command",
    icon="mdi:ev-charger",
    entity_category=EntityCategory.CONFIG,
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select entities from a config entry."""
    code = config_entry.data["code"]
    serial = config_entry.data["serial"]

    async_add_entities([
        ChargepointOperationModeEntity(OPERATION_MODE, serial, code),
        ChargepointLockModeEntity(LOCK_MODE, serial, code),
        ChargepointPauseModeEntity(PAUSE_MODE, serial, code),
    ])


class ChargepointOperationModeEntity(SelectEntity):
    """Entity for selecting the chargepoint power in amps."""

    _attr_should_poll = False

    def __init__(
        self,
        description: SelectEntityDescription,
        serial: str,
        code: str,
    ) -> None:
        self.entity_description = description
        self._attr_unique_id = f"{serial}-{description.key}"
        self._attr_options = CHARGEPOINT_OPERATION_MODES
        self._attr_current_option = None  # No option selected until user picks one
        self.serial = serial
        self.code = code

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.serial)},
            name=f"{NAME} {self.serial}",
            manufacturer=NAME,
            model=VERSION,
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        url = "https://europe-west1-chargesplithome.cloudfunctions.net/secureEndpoint"
        session = requests.Session()
        data = {"SECRET": self.code, "SERIAL": self.serial, "COMMAND": "PILOTCHANGE", "VALUE": option}
        await self.hass.async_add_executor_job(lambda: session.post(url, data=data, verify=False))
        self._attr_current_option = option
        self.async_write_ha_state()


class ChargepointLockModeEntity(SelectEntity):
    """Entity for sending lock/unlock commands."""

    _attr_should_poll = False

    def __init__(
        self,
        description: SelectEntityDescription,
        serial: str,
        code: str,
    ) -> None:
        self.entity_description = description
        self._attr_unique_id = f"{serial}-{description.key}"
        self._attr_options = CHARGEPOINT_LOCK_MODES
        self._attr_current_option = None  # No option selected until user picks one
        self.serial = serial
        self.code = code

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.serial)},
            name=f"{NAME} {self.serial}",
            manufacturer=NAME,
            model=VERSION,
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        url = "https://europe-west1-chargesplithome.cloudfunctions.net/secureEndpoint"
        session = requests.Session()
        data = {"SECRET": self.code, "SERIAL": self.serial, "COMMAND": "LOCK", "VALUE": option}
        await self.hass.async_add_executor_job(lambda: session.post(url, data=data, verify=False))
        self._attr_current_option = option
        self.async_write_ha_state()


class ChargepointPauseModeEntity(SelectEntity):
    """Entity for sending pause/restart commands."""

    _attr_should_poll = False

    def __init__(
        self,
        description: SelectEntityDescription,
        serial: str,
        code: str,
    ) -> None:
        self.entity_description = description
        self._attr_unique_id = f"{serial}-{description.key}"
        self._attr_options = CHARGEPOINT_PAUSE_MODES
        self._attr_current_option = None  # No option selected until user picks one
        self.serial = serial
        self.code = code

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self.serial)},
            name=f"{NAME} {self.serial}",
            manufacturer=NAME,
            model=VERSION,
        )

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        url = "https://europe-west1-chargesplithome.cloudfunctions.net/secureEndpoint"
        session = requests.Session()
        data = {"SECRET": self.code, "SERIAL": self.serial, "COMMAND": "PAUSERESTART", "VALUE": option}
        await self.hass.async_add_executor_job(lambda: session.post(url, data=data, verify=False))
        self._attr_current_option = option
        self.async_write_ha_state()
