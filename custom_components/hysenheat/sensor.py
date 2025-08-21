"""
Support for Hysen Heating Controller sensors.

This module provides sensors for device time.
"""

import logging
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from .const import (
    DOMAIN,
    DATA_KEY_CLOCK_HOUR,
    DATA_KEY_CLOCK_MINUTE,
    DATA_KEY_CLOCK_SECOND,
    DATA_KEY_CLOCK_WEEKDAY,
    HYSENHEAT_WEEKDAY_MONDAY,
    HYSENHEAT_WEEKDAY_SUNDAY,
)
from .entity import HysenEntity

_LOGGER = logging.getLogger(__name__)

# Mapping for weekday numbers to names
WEEKDAY_MAP = {
    HYSENHEAT_WEEKDAY_MONDAY: "Monday",
    HYSENHEAT_WEEKDAY_MONDAY + 1: "Tuesday",
    HYSENHEAT_WEEKDAY_MONDAY + 2: "Wednesday",
    HYSENHEAT_WEEKDAY_MONDAY + 3: "Thursday",
    HYSENHEAT_WEEKDAY_MONDAY + 4: "Friday",
    HYSENHEAT_WEEKDAY_MONDAY + 5: "Saturday",
    HYSENHEAT_WEEKDAY_SUNDAY: "Sunday",
}

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Hysen sensors from a config entry.

    Initializes and adds the sensor entities for the device.

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry containing device details.
        async_add_entities: Callback to add entities asynchronously.

    Returns:
        None
    """
    device_data = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([
        HysenDeviceTimeSensor(device_data),
    ])

class HysenDeviceTimeSensor(HysenEntity, SensorEntity):
    """Representation of a Hysen Device Time sensor.

    Displays the current time and weekday on the device.
    """

    def __init__(self, device_data):
        """Initialize the sensor.

        Args:
            device_data: Dictionary containing device-specific data (e.g., mac, name, coordinator).
        """
        super().__init__(device_data["coordinator"], device_data)
        self._attr_unique_id = f"{device_data['mac']}_device_time"
        self._attr_name = f"{device_data['name']} Device Time"
        self._attr_icon = "mdi:clock"

    @property
    def native_value(self):
        """Return the current device time and weekday as a formatted string.

        Returns:
            str: Formatted string like "Weekday HH:MM:SS" or None if data is incomplete.
        """
        hour = self.coordinator.data.get(DATA_KEY_CLOCK_HOUR)
        minute = self.coordinator.data.get(DATA_KEY_CLOCK_MINUTE)
#        second = self.coordinator.data.get(DATA_KEY_CLOCK_SECOND)
        weekday = self.coordinator.data.get(DATA_KEY_CLOCK_WEEKDAY)

#        if None in (hour, minute, second, weekday):
        if None in (hour, minute, weekday):
            return None

        # Format time as HH:MM:SS
#        time_str = f"{hour:02d}:{minute:02d}:{second:02d}"
        time_str = f"{hour:02d}:{minute:02d}"
        # Get weekday name
        weekday_str = WEEKDAY_MAP.get(weekday, "Unknown")
        return f"{weekday_str} {time_str}"