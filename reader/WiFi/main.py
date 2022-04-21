"""Process data from ESPHome device via Wi-Fi."""
import asyncio
import logging
import sys

from get_data_from_sensor import reader

_LOGGER = logging.getLogger(__name__)


async def process_data(device: reader):
    """Update and process data from device."""
    await device.update()
    _LOGGER.debug(device.data)


if __name__ == "__main__":
    port = None
    host = None

    if sys.argv[2]:
        (host, port) = sys.argv[2].split(":")
    if sys.argv[3]:
        port = sys.argv[3]

    if port is not None:
        port = int(port)
    asyncio.get_event_loop().run_until_complete(
        process_data(reader(password=sys.argv[1], device=host, port=port))
    )
