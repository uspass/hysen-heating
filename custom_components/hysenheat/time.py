"""
Support for Hysen Heating Controller time entities.

This module provides time entities for setting time slots for the Hysen controller.
"""

import logging
import asyncio
import voluptuous as vol
from datetime import time
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.components.time import TimeEntity
from .const import (
    DOMAIN,
    DATA_KEY_SLOT1_TIME,
    DATA_KEY_SLOT2_TIME,
    DATA_KEY_SLOT3_TIME,
    DATA_KEY_SLOT4_TIME,
    DATA_KEY_SLOT5_TIME,
    DATA_KEY_SLOT6_TIME,
    DATA_KEY_SLOT1_WE_TIME,
    DATA_KEY_SLOT2_WE_TIME,
    SERVICE_SET_SLOT1_TIME,
    SERVICE_SET_SLOT2_TIME,
    SERVICE_SET_SLOT3_TIME,
    SERVICE_SET_SLOT4_TIME,
    SERVICE_SET_SLOT5_TIME,
    SERVICE_SET_SLOT6_TIME,
    SERVICE_SET_SLOT1_WE_TIME,
    SERVICE_SET_SLOT2_WE_TIME,
    ATTR_SLOT1_TIME,
    ATTR_SLOT2_TIME,
    ATTR_SLOT3_TIME,
    ATTR_SLOT4_TIME,
    ATTR_SLOT5_TIME,
    ATTR_SLOT6_TIME,
    ATTR_SLOT1_WE_TIME,
    ATTR_SLOT2_WE_TIME,
)
from .entity import HysenEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Hysen time entities from a config entry.

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry containing device details.
        async_add_entities: Callback to add entities asynchronously.

    Returns:
        None
    """
    device_data = hass.data[DOMAIN][config_entry.entry_id]
    _LOGGER.debug("Coordinator data: %s", device_data["coordinator"].data)
    time_entities = [
        HysenSlotTime(device_data, 1, False, DATA_KEY_SLOT1_TIME, SERVICE_SET_SLOT1_TIME, ATTR_SLOT1_TIME, "set_period1"),
        HysenSlotTime(device_data, 2, False, DATA_KEY_SLOT2_TIME, SERVICE_SET_SLOT2_TIME, ATTR_SLOT2_TIME, "set_period2"),
        HysenSlotTime(device_data, 3, False, DATA_KEY_SLOT3_TIME, SERVICE_SET_SLOT3_TIME, ATTR_SLOT3_TIME, "set_period3"),
        HysenSlotTime(device_data, 4, False, DATA_KEY_SLOT4_TIME, SERVICE_SET_SLOT4_TIME, ATTR_SLOT4_TIME, "set_period4"),
        HysenSlotTime(device_data, 5, False, DATA_KEY_SLOT5_TIME, SERVICE_SET_SLOT5_TIME, ATTR_SLOT5_TIME, "set_period5"),
        HysenSlotTime(device_data, 6, False, DATA_KEY_SLOT6_TIME, SERVICE_SET_SLOT6_TIME, ATTR_SLOT6_TIME, "set_period6"),
        HysenSlotTime(device_data, 1, True, DATA_KEY_SLOT1_WE_TIME, SERVICE_SET_SLOT1_WE_TIME, ATTR_SLOT1_WE_TIME, "set_we_period1"),
        HysenSlotTime(device_data, 2, True, DATA_KEY_SLOT2_WE_TIME, SERVICE_SET_SLOT2_WE_TIME, ATTR_SLOT2_WE_TIME, "set_we_period2"),
    ]
    async_add_entities(time_entities)

    platform = entity_platform.async_get_current_platform()
    for slot, is_weekend, service, attr in [
        (1, False, SERVICE_SET_SLOT1_TIME, ATTR_SLOT1_TIME),
        (2, False, SERVICE_SET_SLOT2_TIME, ATTR_SLOT2_TIME),
        (3, False, SERVICE_SET_SLOT3_TIME, ATTR_SLOT3_TIME),
        (4, False, SERVICE_SET_SLOT4_TIME, ATTR_SLOT4_TIME),
        (5, False, SERVICE_SET_SLOT5_TIME, ATTR_SLOT5_TIME),
        (6, False, SERVICE_SET_SLOT6_TIME, ATTR_SLOT6_TIME),
        (1, True, SERVICE_SET_SLOT1_WE_TIME, ATTR_SLOT1_WE_TIME),
        (2, True, SERVICE_SET_SLOT2_WE_TIME, ATTR_SLOT2_WE_TIME),
    ]:
        platform.async_register_entity_service(
            service,
            {
                vol.Required(attr): vol.Any(
                    vol.All(
                        vol.Coerce(str),
                        vol.Datetime("%H:%M:%S", msg="Invalid time format, use HH:MM:SS")
                    ),
                    vol.All(
                        vol.Coerce(str),
                        vol.Datetime("%H:%M", msg="Invalid time format, use HH:MM")
                    )
                ),
            },
            f"async_set_slot{slot}_time" if not is_weekend else f"async_set_slot{slot}_we_time",
        )

class HysenSlotTime(HysenEntity, TimeEntity):
    """Representation of a Hysen time slot entity."""

    def __init__(self, device_data, slot: int, is_weekend: bool, data_key: str, service: str, attr: str, device_method: str):
        """Initialize the time entity.

        Args:
            device_data: Dictionary containing device-specific data.
            slot: The slot number (1–6 for weekdays, 1–2 for weekends).
            is_weekend: True if the slot is for a weekend, False for weekday.
            data_key: The key to retrieve the time value from coordinator.data.
            service: The service name for setting the time.
            attr: The attribute name for the service schema.
            device_method: The device method to call to set the time.
        """
        super().__init__(device_data["coordinator"], device_data)
        self._slot = slot
        self._is_weekend = is_weekend
        self._data_key = data_key
        self._service = service
        self._attr = attr
        self._device_method = device_method
        self._attr_unique_id = f"{device_data['mac']}_slot{slot}{'_we' if is_weekend else ''}_time"
        self._attr_name = f"{device_data['name']} Slot {'We ' if is_weekend else ''}{slot} Time"
        self._attr_icon = "mdi:clock-start"
        self._attr_entity_registry_enabled_default = True

    @property
    def native_value(self):
        """Return the current time value for the slot.

        Returns:
            time: The current time value, or None if unavailable.
        """
        time_str = self.coordinator.data.get(self._data_key)
        if time_str:
            try:
                hour, minute = map(int, time_str.split(":"))
                return time(hour, minute)
            except ValueError:
                _LOGGER.error("[%s] Invalid time format for %s: %s", self._host, self._data_key, time_str)
                return None
        _LOGGER.debug("[%s] No time value for %s", self._host, self._data_key)
        return None

    async def async_set_value(self, value: time):
        """Set the time value for the slot.

        Args:
            value: The time value to set (as a datetime.time object).

        Returns:
            None
        """
        _LOGGER.debug("[%s] Setting slot %s%s time to %s", self._host, self._slot, "_we" if self._is_weekend else "", value)
        success = await self._async_try_command(
            f"Error in {self._device_method}",
            getattr(self.coordinator.device, self._device_method),
            value.hour,
            value.minute,
            None,
        )
        if success:
            # Update coordinator.data to reflect the new value
            self.coordinator.data[self._data_key] = value.strftime("%H:%M")
            await asyncio.sleep(0.2)
            # Force an immediate update to fetch the latest device state
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_slot_time(self, slot_time: str):
        """Set the slot time value (for service calls).

        Args:
            slot_time: The time to set in "HH:MM" or "HH:MM:SS" format.

        Returns:
            None
        """
        try:
            # Try HH:MM:SS format
            time_value = time.fromisoformat(slot_time)
        except ValueError:
            try:
                # Fallback to HH:MM format
                hour, minute = map(int, slot_time.split(":"))
                time_value = time(hour, minute)
            except ValueError:
                _LOGGER.error("[%s] Invalid time format for %s: %s", self._host, self._attr, slot_time)
                raise ValueError(f"Invalid time format for {self._attr}: {slot_time}, use HH:MM or HH:MM:SS")
        await self.async_set_value(time_value)

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        Returns:
            None
        """
        super()._handle_coordinator_update()
        self.async_write_ha_state()
