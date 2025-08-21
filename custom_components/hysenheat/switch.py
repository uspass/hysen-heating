"""
Support for Hysen Heating Coil Controller switches.

This module provides switches for frost protection, and schedule slots.
"""

import logging
import asyncio
import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.components.switch import SwitchEntity
from .const import (
    DOMAIN,
    DATA_KEY_FROST_PROTECTION,
#    DATA_KEY_SLOT1_OFF,
#    DATA_KEY_SLOT2_OFF,
#    DATA_KEY_SLOT3_OFF,
#    DATA_KEY_SLOT4_OFF,
#    DATA_KEY_SLOT5_OFF,
#    DATA_KEY_SLOT6_OFF,
#    DATA_KEY_SLOT1_WE_OFF,
#    DATA_KEY_SLOT2_WE_OFF,
    STATE_ON,
    STATE_OFF,
    ATTR_FROST_PROTECTION,
#    ATTR_SLOT1_OFF,
#    ATTR_SLOT2_OFF,
#    ATTR_SLOT3_OFF,
#    ATTR_SLOT4_OFF,
#    ATTR_SLOT5_OFF,
#    ATTR_SLOT6_OFF,
#    ATTR_SLOT1_WE_OFF,
#    ATTR_SLOT2_WE_OFF,
    SERVICE_SET_FROST_PROTECTION,
#    SERVICE_SET_SLOT1_OFF,
#    SERVICE_SET_SLOT2_OFF,
#    SERVICE_SET_SLOT3_OFF,
#    SERVICE_SET_SLOT4_OFF,
#    SERVICE_SET_SLOT5_OFF,
#    SERVICE_SET_SLOT6_OFF,
#    SERVICE_SET_SLOT1_WE_OFF,
#    SERVICE_SET_SLOT2_WE_OFF,
#    FROST_PROTECTION_HASS_TO_HYSEN,
)
from .entity import HysenEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Hysen switches from a config entry.

    Initializes and adds the switch entities for the device, and registers services.

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry containing device details.
        async_add_entities: Callback to add entities asynchronously.

    Returns:
        None
    """
    device_data = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([
        HysenFrostProtectionSwitch(device_data),
#        HysenSlot1OffSwitch(device_data),
    ])

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SET_FROST_PROTECTION,
        {vol.Required(ATTR_FROST_PROTECTION): vol.In([STATE_ON, STATE_OFF])},
        "async_set_frost_protection",
    )

#    platform.async_register_entity_service(
#        SERVICE_SET_SLOT1_OFF,
#        {vol.Required(ATTR_SLOT1_OFF): vol.In([STATE_ON, STATE_OFF])},
#        "async_set_slot1_off",
#    )

#    platform.async_register_entity_service(
#        SERVICE_SET_SLOT2_OFF,
#        {vol.Required(ATTR_SLOT2_OFF): vol.In([STATE_ON, STATE_OFF])},
#        "async_set_slot2_off",
#    )

#    platform.async_register_entity_service(
#        SERVICE_SET_SLOT3_OFF,
#        {vol.Required(ATTR_SLOT3_OFF): vol.In([STATE_ON, STATE_OFF])},
#        "async_set_slot3_off",
#    )

#    platform.async_register_entity_service(
#        SERVICE_SET_SLOT4_OFF,
#        {vol.Required(ATTR_SLOT4_OFF): vol.In([STATE_ON, STATE_OFF])},
#        "async_set_slot4_off",
#    )

#    platform.async_register_entity_service(
#        SERVICE_SET_SLOT5_OFF,
#        {vol.Required(ATTR_SLOT5_OFF): vol.In([STATE_ON, STATE_OFF])},
#        "async_set_slot5_off",
#    )

#    platform.async_register_entity_service(
#        SERVICE_SET_SLOT6_OFF,
#        {vol.Required(ATTR_SLOT6_OFF): vol.In([STATE_ON, STATE_OFF])},
#        "async_set_slot6_off",
#    )

#    platform.async_register_entity_service(
#        SERVICE_SET_SLOT1_WE_OFF,
#        {vol.Required(ATTR_SLOT1_WE_OFF): vol.In([STATE_ON, STATE_OFF])},
#        "async_set_slot1_we_off",
#    )

#    platform.async_register_entity_service(
#        SERVICE_SET_SLOT2_WE_OFF,
#        {vol.Required(ATTR_SLOT2_WE_OFF): vol.In([STATE_ON, STATE_OFF])},
#        "async_set_slot2_we_off",
#    )

class HysenFrostProtectionSwitch(HysenEntity, SwitchEntity):
    """Representation of a Hysen Frost Protection switch.

    Controls whether frost protection is enabled or disabled.
    """

    def __init__(self, device_data):
        """Initialize the switch.

        Args:
            device_data: Dictionary containing device-specific data (e.g., mac, name, coordinator).
        """
        super().__init__(device_data["coordinator"], device_data)
        self._attr_unique_id = f"{device_data['mac']}_frost_protection"
        self._attr_name = f"{device_data['name']} Frost Protection"

    @property
    def is_on(self):
        """Return true if the switch is on.

        Returns:
            bool: True if frost protection is on, False otherwise.
        """
        return self.coordinator.data.get(DATA_KEY_FROST_PROTECTION) == STATE_ON

    @property
    def icon(self):
        """Return the icon based on the switch state.

        Returns:
            str: The Material Design Icon (MDI) for the frost protection state.
        """
        return "mdi:snowflake" if self.is_on else "mdi:snowflake-off"

    async def async_turn_on(self, **kwargs):
        """Turn the switch on.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        _LOGGER.debug("[%s] Turning on frost protection", self._host)
        success = await self._async_try_command(
            "Error in set_frost_protection",
            self.coordinator.device.set_frost_protection,
            FROST_PROTECTION_HASS_TO_HYSEN[STATE_ON],
        )
        if success:
            # Delay to allow device to stabilize
            await asyncio.sleep(0.2)
            # Force an immediate update to fetch the latest device state
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            None
        """
        _LOGGER.debug("[%s] Turning off frost protection", self._host)
        success = await self._async_try_command(
            "Error in set_frost_protection",
            self.coordinator.device.set_frost_protection,
            FROST_PROTECTION_HASS_TO_HYSEN[STATE_OFF],
        )
        if success:
            # Delay to allow device to stabilize
            await asyncio.sleep(0.2)
            # Force an immediate update to fetch the latest device state
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_frost_protection(self, frost_protection):
        """Set the frost protection state.

        Args:
            frost_protection: The state to set (on or off).

        Returns:
            None
        """
        _LOGGER.debug("[%s] Setting frost protection to %s", self._host, frost_protection)
        success = await self._async_try_command(
            "Error in set_frost_protection",
            self.coordinator.device.set_frost_protection,
            FROST_PROTECTION_HASS_TO_HYSEN[frost_protection],
        )
        if success:
            # Delay to allow device to stabilize
            await asyncio.sleep(0.2)
            # Force an immediate update to fetch the latest device state
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

