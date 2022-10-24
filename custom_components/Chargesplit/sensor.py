import logging
import requests
import json

from decimal import Decimal

from homeassistant.config_entries import ConfigEntry

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)

from homeassistant.const import (
    PERCENTAGE,
    TIME_DAYS,
    VOLUME_LITERS,
    MASS_KILOGRAMS,
    ELECTRIC_CURRENT_AMPERE,
    ENERGY_KILO_WATT_HOUR,
    LENGTH_KILOMETERS,
    TEMP_CELSIUS,
    ELECTRIC_POTENTIAL_VOLT,
    POWER_KILO_WATT
)

from .const import DOMAIN
from .entity import ChargesplitEntity
from .coordinator import ChargesplitDataUpdateCoordinator

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    coordinator = hass.data[DOMAIN]

    INSTRUMENTS = [
        (
            "power_voltagel2",
            "Voltage L2",
            "VOLT2",
            ELECTRIC_POTENTIAL_VOLT,
            "mdi:lightning-bolt",
            SensorStateClass.MEASUREMENT,
        ),
        (
            "power_voltagel1",
            "Voltage L1",
            "VOLT1",
            ELECTRIC_POTENTIAL_VOLT,
            "mdi:lightning-bolt",
            SensorStateClass.MEASUREMENT,
        ),
        (
            "power_voltagel3",
            "Voltage L3",
            "VOLT3",
            ELECTRIC_POTENTIAL_VOLT,
            "mdi:lightning-bolt",
            SensorStateClass.MEASUREMENT,
        ),
        (
            "device_temperature",
            "Temperature",
            "TEMP",
            TEMP_CELSIUS,
            "mdi:temperature-celsius",
            SensorStateClass.MEASUREMENT,
        ),
        (
            "device_status",
            "Wallbox Status",
            "STATUS",
            None,
            "mdi:ev-station",
            None,
        ),
         (
            "device_model",
            "Wallbox Model",
            "MODEL",
            None,
            "mdi:ev-station",
            None,
        ),
         (
            "device_firmware",
            "Wallbox firmware",
            "FWVERS",
            None,
            "mdi:ev-station",
            None,
        ),
         (
            "device_serial",
            "Wallbox serial",
            "SERIAL",
            None,
            "mdi:ev-station",
            None,
        ),
        (
            "power_charged_kWh",
            "Charged kWh",
            "TOTALCHARGED",
            ENERGY_KILO_WATT_HOUR,
            "mdi:speedometer",
            SensorDeviceClass.ENERGY,
        ),
        (
            "power_pilotamps",
            "Pilot Amps",
            "PILOTLIMIT",
            ELECTRIC_CURRENT_AMPERE,
            "mdi:speedometer",
            SensorDeviceClass.CURRENT,
        ),
        (
            "power_solar_power",
            "Generated solar power",
            "SOLARPWR",
            POWER_KILO_WATT,
            "mdi:speedometer",
            SensorDeviceClass.POWER,
        ),
        (
            "power_house_power",
            "House Consumption",
            "HOUSEPWR",
            POWER_KILO_WATT,
            "mdi:speedometer",
            SensorDeviceClass.POWER,
        ),
        (
            "power_car_charging",
            "Car Charging Power",
            "CHARGINGPWR",
            POWER_KILO_WATT,
            "mdi:speedometer",
            SensorDeviceClass.POWER,
        ),    
          
    ]

    sensors = [
        ChargesplitSensor(
            coordinator, entry, id, description, key, unit, icon, device_class
        )
        for id, description, key, unit, icon, device_class in INSTRUMENTS
    ]

    async_add_devices(sensors, True)


class ChargesplitSensor(ChargesplitEntity):
    def __init__(
        self,
        coordinator: ChargesplitDataUpdateCoordinator,
        entry: ConfigEntry,
        id: str,
        description: str,
        key: str,
        unit: str,
        icon: str,
        device_class: str,
    ):
        super().__init__(coordinator, entry)
        self._id = id
        self.description = description
        self.key = key
        self.unit = unit
        self._icon = icon
        self._device_class = device_class

    




    @property
    def state(self):
        a = json.loads(self.coordinator.data)
        return a[self.key]

    @property
    def unit_of_measurement(self):
        return self.unit

    @property
    def icon(self):
        return self._icon

    @property
    def device_class(self):
        return self._device_class

    @property
    def name(self):
        return f"{self.description}"

    @property
    def id(self):
        return f"{DOMAIN}_{self._id}"

    @property
    def unique_id(self):
        return f"{DOMAIN}-{self._id}-{self.coordinator.api.host}"
