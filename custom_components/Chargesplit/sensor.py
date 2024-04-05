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

    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature
)

from .const import DOMAIN
from .entity import ChargesplitEntity
from .coordinator import ChargesplitDataUpdateCoordinator

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    coordinator = hass.data[DOMAIN]
    serial = entry.data["serial"]

    INSTRUMENTS = [
        (
            "power_voltagel2",
            "Voltage L2",
            "VOLT2",
            UnitOfElectricPotential.VOLT,
            "mdi:lightning-bolt",
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
            serial,
        ),
        (
            "power_voltagel1",
            "Voltage L1",
            "VOLT1",
            UnitOfElectricPotential.VOLT,
            "mdi:lightning-bolt",
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
            serial,
        ),
        (
            "power_voltagel3",
            "Voltage L3",
            "VOLT3",
            UnitOfElectricPotential.VOLT,
            "mdi:lightning-bolt",
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
            serial,
        ),
        (
            "device_temperature",
            "Temperature",
            "TEMP",
            UnitOfTemperature.CELSIUS,
            "mdi:temperature-celsius",
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            serial,
        ),
        (
            "device_status",
            "Wallbox Status",
            "STATUS",
            None,
            "mdi:ev-station",
            None,
            None,
            serial,
        ),
        (
            "device_model",
            "Wallbox Model",
            "MODEL",
            None,
            "mdi:ev-station",
            None,
            None,
            serial,
        ),
        (
            "device_firmware",
            "Wallbox firmware",
            "FWVERS",
            None,
            "mdi:ev-station",
            None,
            None,
            serial,
        ),
        (
            "device_serial",
            "Wallbox serial",
            "SERIAL",
            None,
            "mdi:ev-station",
            None,
            None,
            serial,
        ),
        (
            "power_charged_kWh",
            "Charged kWh",
            "TOTALCHARGED",
            UnitOfEnergy.KILO_WATT_HOUR,
            "mdi:speedometer",
            SensorDeviceClass.ENERGY,
            SensorStateClass.TOTAL_INCREASING,
            serial,
        ),
        (
            "power_pilotamps",
            "Pilot Amps",
            "PILOTLIMIT",
            UnitOfElectricCurrent.AMPERE,
            "mdi:speedometer",
            SensorDeviceClass.CURRENT,
            SensorStateClass.MEASUREMENT,
            serial,
        ),
        (
            "power_solar_power",
            "Generated solar power",
            "SOLARPWR",
            UnitOfPower.KILO_WATT,
            "mdi:speedometer",
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
            serial,
        ),
        (
            "power_house_power",
            "House Consumption",
            "HOUSEPWR",
            UnitOfPower.KILO_WATT,
            "mdi:speedometer",
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
            serial,
        ),
        (
            "power_car_charging",
            "Car Charging Power",
            "CHARGINGPWR",
            UnitOfPower.KILO_WATT,
            "mdi:speedometer",
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
            serial,
        ),    
        
    ]

    sensors = [
        ChargesplitSensor(
            coordinator, entry, id, description, key, unit, icon, device_class, device_status, serial
        )
        for id, description, key, unit, icon, device_class, device_status, serial in INSTRUMENTS
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
        device_status: str,
        serial,
    ):
        super().__init__(coordinator, entry)
        self._id = f"{serial}-{description}"
        self.description = description
        self.key = key
        self.unit = unit
        self._icon = icon
        self._device_class = device_class
        self._device_status = device_status
    




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
    def device_status(self):
        return self._device_status

    @property
    def name(self):
        return f"{self.description}"

    @property
    def id(self):
        return f"{DOMAIN}_{self._id}"

    @property
    def unique_id(self):
        return f"{DOMAIN}-{self._id}-{self.coordinator.api.host}"
