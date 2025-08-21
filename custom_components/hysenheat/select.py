"""
Support for Hysen Heating Controller select entities.

This module provides select entities for setting the key lock and sensor type values.
"""

import logging
import asyncio
import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.components.select import SelectEntity
from .const import (
    DOMAIN,
    DATA_KEY_KEY_LOCK,
    DATA_KEY_SENSOR_TYPE,
    ATTR_KEY_LOCK,
    ATTR_SENSOR_TYPE,
    SERVICE_SET_KEY_LOCK,
    SERVICE_SET_SENSOR_TYPE,
    STATE_UNLOCKED,
    STATE_LOCKED,
    STATE_SENSOR_INTERNAL,
    STATE_SENSOR_EXTERNAL,
    STATE_SENSOR_INT_EXT,
    KEY_LOCK_HASS_TO_HYSEN,
    SENSOR_TYPE_HASS_TO_HYSEN,
)
from .entity import HysenEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Hysen select entities from a config entry.

    Initializes and adds the select entities for the device, and registers services.

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry containing device details.
        async_add_entities: Callback to add entities asynchronously.

    Returns:
        None
    """
    device_data = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([
        HysenKeyLockSelect(device_data),
        HysenSensorTypeSelect(device_data),
    ])

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SET_KEY_LOCK,
        {vol.Required(ATTR_KEY_LOCK): vol.In([STATE_UNLOCKED, STATE_LOCKED])},
        "async_set_key_lock",
    )
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SET_SENSOR_TYPE,
        {vol.Required(ATTR_SENSOR_TYPE): vol.In([STATE_SENSOR_INTERNAL, STATE_SENSOR_EXTERNAL, STATE_SENSOR_INT_EXT])},
        "async_set_sensor_type",
    )

class HysenKeyLockSelect(HysenEntity, SelectEntity):
    """Representation of a Hysen Key Lock select entity.

    Allows selection of key lock modes.
    """

    def __init__(self, device_data):
        """Initialize the select entity.

        Args:
            device_data: Dictionary containing device-specific data (e.g., mac, name, coordinator).
        """
        super().__init__(device_data["coordinator"], device_data)
        self._attr_unique_id = f"{device_data['mac']}_key_lock"
        self._attr_name = f"{device_data['name']} Key Lock"
        self._attr_options = [STATE_UNLOCKED, STATE_LOCKED]

    @property
    def icon(self):
        """Return the icon based on the current key lock state.

        Returns:
            str: The Material Design Icon (MDI) for the key lock state.
        """
        icons = {
            STATE_UNLOCKED: "mdi:lock-open-variant",
            STATE_LOCKED: "mdi:lock",
        }
        return icons.get(self.current_option, "mdi:lock")

    @property
    def current_option(self):
        """Return the current selected key lock option.

        Returns:
            str: The current key lock state.
        """
        return self.coordinator.data.get(DATA_KEY_KEY_LOCK)

    async def async_select_option(self, option: str):
        """Set the key lock option.

        Args:
            option: The key lock option to set.

        Returns:
            None
        """
        _LOGGER.debug("[%s] Setting key lock to %s", self._host, option)
        success = await self._async_try_command(
            "Error in set_key_lock",
            self.coordinator.device.set_key_lock,
            KEY_LOCK_HASS_TO_HYSEN[option],
        )
        if success:
            # Delay to allow device to stabilize
            await asyncio.sleep(0.2)
            # Force an immediate update to fetch the latest device state
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_key_lock(self, key_lock):
        """Set the key lock state (for service calls).

        Args:
            key_lock: The key lock value to set.

        Returns:
            None
        """
        await self.async_select_option(key_lock)

class HysenSensorTypeSelect(HysenEntity, SelectEntity):
    """Representation of a Hysen Sensor Type select entity.

    Allows selection of sensor type modes.
    """

    def __init__(self, device_data):
        """Initialize the select entity.

        Args:
            device_data: Dictionary containing device-specific data (e.g., mac, name, coordinator).
        """
        super().__init__(device_data["coordinator"], device_data)
        self._attr_unique_id = f"{device_data['mac']}_sensor_type"
        self._attr_name = f"{device_data['name']} Sensor Type"
        self._attr_options = [STATE_SENSOR_INTERNAL, STATE_SENSOR_EXTERNAL, STATE_SENSOR_INT_EXT]
        self._attr_icon = "mdi:thermometer"

    @property
    def current_option(self):
        """Return the current selected sensor type option.

        Returns:
            str: The current sensor type state.
        """
        return self.coordinator.data.get(DATA_KEY_SENSOR_TYPE)

    async def async_select_option(self, option: str):
        """Set the sensor type option.

        Args:
            option: The sensor type option to set.

        Returns:
            None
        """
        _LOGGER.debug("[%s] Setting sensor type to %s", self._host, option)
        success = await self._async_try_command(
            "Error in set_sensor",
            self.coordinator.device.set_sensor,
            SENSOR_TYPE_HASS_TO_HYSEN[option],
        )
        if success:
            # Delay to allow device to stabilize
            await asyncio.sleep(0.2)
            # Force an immediate update to fetch the latest device state
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_sensor_type(self, sensor_type):
        """Set the sensor type state (for service calls).

        Args:
            sensor_type: sensor type value to set.

        Returns:
            None
        """
        await self.async_select_option(sensor_type)