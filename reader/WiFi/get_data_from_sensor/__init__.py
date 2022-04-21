"""Get data from ESPHome device via native API."""

from dataclasses import dataclass
from datetime import datetime

import aioesphomeapi


@dataclass(init=False)
class sensorData:
    """Sensor data."""

    api_version: str = None
    """version of the device API"""
    device_info: aioesphomeapi.DeviceInfo = None

    co2_value: int = None
    """Current Co2 readings"""
    last_update: datetime = None
    """When las update occurs"""


class reader:
    """Read data from the sensor."""

    default_address: str = "co2_sensor.local"
    default_port: int = 6053
    _data = sensorData()

    def __init__(
        self, password: str, device: str | None = None, port: int | None = None
    ):
        """Reader initialization.

        :param device: sensor address for connect to
        :param port: API port
        :param password: API password for device
        """
        self.__address = device or self.default_address
        self.__port = port or self.default_port
        self.__password = password

    async def update(self):
        """Connect to an ESPHome device and update data."""
        # Establish connection
        api = aioesphomeapi.APIClient(self.__address, self.__port, self.__password)
        await api.connect(login=True)

        self._data.api_version = api.api_version
        self._data.device_info = await api.device_info()

        # List all entities of the device
        entities = await api.list_entities_services()
        print(entities)

    @property
    def data(self) -> sensorData:
        """Device data."""
        return self._data
