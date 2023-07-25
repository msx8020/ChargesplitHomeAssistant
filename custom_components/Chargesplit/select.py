import logging
import requests
import asyncio
from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import Event, HomeAssistant
from homeassistant.helpers import entity_registry
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event
from .api import ChargesplitApi
from .const import DOMAIN,CONF_CODE,CHARGEPOINT_SERIAL
from .coordinator import ChargesplitDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


CHARGEPOINT_OPERATION_MODES = [
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
]


CHARGEPOINT_LOCK_MODES = [
    "LOCK",
    "UNLOCK",
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




async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
    
) -> None:
    """Set up the inverter select entities from a config entry."""
    coordinator = hass.data[DOMAIN]
    code = config_entry.data.get(CONF_CODE)
    serial = config_entry.data.get(CHARGEPOINT_SERIAL)
    
    entity = ChargepointOperationModeEntity(
    OPERATION_MODE,
    "SELECT POWER",
    serial,
    code,
    )
    async_add_entities([entity])

    entity2 = ChargepointLockModeEntity(
    LOCK_MODE,
    "SELECT LOCK OR UNLOCK",
    serial,
    code,
    )
    async_add_entities([entity2])

class ChargepointOperationModeEntity(SelectEntity):
    """Entity representing the inverter operation mode."""

    _attr_should_poll = False
    
    def __init__(
        self,
        description: SelectEntityDescription,
        current_mode: str,
        serial: str,
        code: str,
        
    ) -> None:
        """Initialize the inverter operation mode setting entity."""
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}-{description.key}"
        self._attr_options = CHARGEPOINT_OPERATION_MODES
        self._attr_current_option = current_mode
        self.serial = serial
        self.code = code 

    async def async_select_option(
        self, option: str
        ) -> None:
        
        """Change the selected option."""
        url = "https://europe-west1-chargesplithome.cloudfunctions.net/secureEndpoint"
        session = requests.Session()
        data = { "SECRET": self.code, "SERIAL": self.serial, "COMMAND": "PILOTCHANGE","VALUE":option}   
        result =  await self.hass.async_add_executor_job(lambda:  session.post(url, data=data, verify=False))
        
        

class ChargepointLockModeEntity(SelectEntity):
    """Entity representing the inverter operation mode."""

    _attr_should_poll = False
    def __init__(
        self,
        description: SelectEntityDescription,
        current_mode: str,
        serial: str,
        code: str,
    ) -> None:
        """Initialize the inverter operation mode setting entity."""
        self.entity_description = description
        self._attr_unique_id = f"{DOMAIN}-{description.key}"
        self._attr_options = CHARGEPOINT_LOCK_MODES
        self._attr_current_option = current_mode
        self.serial = serial
        self.code = code 

    async def async_select_option(
        self, option: str
        ) -> None:
        """Change the selected option."""
        url = "https://europe-west1-chargesplithome.cloudfunctions.net/secureEndpoint"
        session = requests.Session()
        _LOGGER.warning(option)
        data = { "SECRET": self.code, "SERIAL": self.serial, "COMMAND": "LOCK","VALUE":option}   
        result =  await self.hass.async_add_executor_job(lambda:  session.post(url, data=data, verify=False))
        
        