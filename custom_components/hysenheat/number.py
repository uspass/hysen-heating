"""
Support for Hysen Heating Controller number entities.

This module provides number entities for setting calibration, dynamic max/min temperatures and slot temperatures.
"""

import logging
import asyncio
import voluptuous as vol
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import entity_platform
from homeassistant.components.number import NumberEntity
from .const import (
    DOMAIN,
    PRECISION_WHOLE,
    PRECISION_HALVES,
    UnitOfTemperature,
    HVACMode,
    STATE_OFF,
    DATA_KEY_TARGET_TEMP,
    DATA_KEY_POWER_STATE,
    DATA_KEY_OPERATION_MODE,
    DATA_KEY_TEMPORARY_MANUAL,
    DATA_KEY_HYSTERESIS,
    DATA_KEY_MAX_TEMP,
    DATA_KEY_MIN_TEMP,
    DATA_KEY_CALIBRATION,
    DATA_KEY_SLOT1_TEMP,
    DATA_KEY_SLOT2_TEMP,
    DATA_KEY_SLOT3_TEMP,
    DATA_KEY_SLOT4_TEMP,
    DATA_KEY_SLOT5_TEMP,
    DATA_KEY_SLOT6_TEMP,
    DATA_KEY_SLOT1_WE_TEMP,
    DATA_KEY_SLOT2_WE_TEMP,
    ATTR_HYSTERESIS,
    ATTR_MAX_TEMP,
    ATTR_MIN_TEMP,
    ATTR_CALIBRATION,
    ATTR_SLOT1_TEMP,
    ATTR_SLOT2_TEMP,
    ATTR_SLOT3_TEMP,
    ATTR_SLOT4_TEMP,
    ATTR_SLOT5_TEMP,
    ATTR_SLOT6_TEMP,
    ATTR_SLOT1_WE_TEMP,
    ATTR_SLOT2_WE_TEMP,
    SERVICE_SET_HYSTERESIS,
    SERVICE_SET_MAX_TEMP,
    SERVICE_SET_MIN_TEMP,
    SERVICE_SET_CALIBRATION,
    SERVICE_SET_SLOT1_TEMP,
    SERVICE_SET_SLOT2_TEMP,
    SERVICE_SET_SLOT3_TEMP,
    SERVICE_SET_SLOT4_TEMP,
    SERVICE_SET_SLOT5_TEMP,
    SERVICE_SET_SLOT6_TEMP,
    SERVICE_SET_SLOT1_WE_TEMP,
    SERVICE_SET_SLOT2_WE_TEMP,
    HYSENHEAT_HYSTERESIS_MIN,
    HYSENHEAT_HYSTERESIS_MAX,
    HYSENHEAT_MAX_TEMP,
    HYSENHEAT_MIN_TEMP,
    HYSENHEAT_CALIBRATION_MIN,
    HYSENHEAT_CALIBRATION_MAX,
    HYSENHEAT_DEFAULT_MAX_TEMP,
    HYSENHEAT_DEFAULT_MIN_TEMP,
    MODE_HASS_TO_HYSEN,
)
from .entity import HysenEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Hysen number entities from a config entry.

    Args:
        hass: The Home Assistant instance.
        config_entry: The configuration entry containing device details.
        async_add_entities: Callback to add entities asynchronously.

    Returns:
        None
    """
    device_data = hass.data[DOMAIN][config_entry.entry_id]
    _LOGGER.debug("Coordinator data: %s", device_data["coordinator"].data)
    entities = [
        HysenHysteresisNumber(device_data),
        HysenMaxTempNumber(device_data),
        HysenCalibrationNumber(device_data),
        HysenMinTempNumber(device_data),
        HysenSlotTempNumber(device_data, 1, False, DATA_KEY_SLOT1_TEMP, SERVICE_SET_SLOT1_TEMP, ATTR_SLOT1_TEMP, "set_period1"),
        HysenSlotTempNumber(device_data, 2, False, DATA_KEY_SLOT2_TEMP, SERVICE_SET_SLOT2_TEMP, ATTR_SLOT2_TEMP, "set_period2"),
        HysenSlotTempNumber(device_data, 3, False, DATA_KEY_SLOT3_TEMP, SERVICE_SET_SLOT3_TEMP, ATTR_SLOT3_TEMP, "set_period3"),
        HysenSlotTempNumber(device_data, 4, False, DATA_KEY_SLOT4_TEMP, SERVICE_SET_SLOT4_TEMP, ATTR_SLOT4_TEMP, "set_period4"),
        HysenSlotTempNumber(device_data, 5, False, DATA_KEY_SLOT5_TEMP, SERVICE_SET_SLOT5_TEMP, ATTR_SLOT5_TEMP, "set_period5"),
        HysenSlotTempNumber(device_data, 6, False, DATA_KEY_SLOT6_TEMP, SERVICE_SET_SLOT6_TEMP, ATTR_SLOT6_TEMP, "set_period6"),
        HysenSlotTempNumber(device_data, 1, True, DATA_KEY_SLOT1_WE_TEMP, SERVICE_SET_SLOT1_WE_TEMP, ATTR_SLOT1_WE_TEMP, "set_we_period1"),
        HysenSlotTempNumber(device_data, 2, True, DATA_KEY_SLOT2_WE_TEMP, SERVICE_SET_SLOT2_WE_TEMP, ATTR_SLOT2_WE_TEMP, "set_we_period2"),
    ]
    async_add_entities(entities)

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SET_HYSTERESIS,
        {
            vol.Required(ATTR_HYSTERESIS): vol.All(
                vol.Coerce(float),
                vol.Range(min=HYSENHEAT_HYSTERESIS_MIN, max=HYSENHEAT_HYSTERESIS_MAX)
            )
        },
        "async_set_hysteresis",
    )
    platform.async_register_entity_service(
        SERVICE_SET_MAX_TEMP,
        {
            vol.Required(ATTR_MAX_TEMP): vol.All(
                vol.Coerce(int),
                vol.Range(min=HYSENHEAT_MIN_TEMP, max=HYSENHEAT_MAX_TEMP)
            )
        },
        "async_set_max_temp",
    )
    platform.async_register_entity_service(
        SERVICE_SET_MIN_TEMP,
        {
            vol.Required(ATTR_MIN_TEMP): vol.All(
                vol.Coerce(int),
                vol.Range(min=HYSENHEAT_MIN_TEMP, max=HYSENHEAT_MAX_TEMP)
            )
        },
        "async_set_min_temp",
    )
    platform.async_register_entity_service(
        SERVICE_SET_CALIBRATION,
        {
            vol.Required(ATTR_CALIBRATION): vol.All(
                vol.Coerce(float),
                vol.Range(min=HYSENHEAT_CALIBRATION_MIN, max=HYSENHEAT_CALIBRATION_MAX)
            )
        },
        "async_set_calibration",
    )
    for slot, is_weekend, service, attr in [
        (1, False, SERVICE_SET_SLOT1_TEMP, ATTR_SLOT1_TEMP),
        (2, False, SERVICE_SET_SLOT2_TEMP, ATTR_SLOT2_TEMP),
        (3, False, SERVICE_SET_SLOT3_TEMP, ATTR_SLOT3_TEMP),
        (4, False, SERVICE_SET_SLOT4_TEMP, ATTR_SLOT4_TEMP),
        (5, False, SERVICE_SET_SLOT5_TEMP, ATTR_SLOT5_TEMP),
        (6, False, SERVICE_SET_SLOT6_TEMP, ATTR_SLOT6_TEMP),
        (1, True, SERVICE_SET_SLOT1_WE_TEMP, ATTR_SLOT1_WE_TEMP),
        (2, True, SERVICE_SET_SLOT2_WE_TEMP, ATTR_SLOT2_WE_TEMP),
    ]:
        platform.async_register_entity_service(
            service,
            {
                vol.Required(attr): vol.All(
                    vol.Coerce(float),
                    vol.Range(min=HYSENHEAT_DEFAULT_MIN_TEMP, max=HYSENHEAT_DEFAULT_MAX_TEMP)
                )
            },
            f"async_set_slot{slot}_temp" if not is_weekend else f"async_set_slot{slot}_we_temp",
        )

class HysenHysteresisNumber(HysenEntity, NumberEntity):
    """Representation of a Hysen Hysteresis number entity."""

    def __init__(self, device_data):
        """Initialize the number entity.

        Args:
            device_data: Dictionary containing device-specific data.
        """
        super().__init__(device_data["coordinator"], device_data)
        self._attr_unique_id = f"{device_data['mac']}_hysteresis"
        self._attr_name = f"{device_data['name']} Hysteresis"
        self._attr_native_min_value = HYSENHEAT_HYSTERESIS_MIN
        self._attr_native_max_value = HYSENHEAT_HYSTERESIS_MAX
        self._attr_native_step = PRECISION_WHOLE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"

    @property
    def native_value(self):
        """Return the current hysteresis value.

        Returns:
            float: The current hysteresis.
        """
        return self.coordinator.data.get(DATA_KEY_HYSTERESIS)

    async def async_set_native_value(self, value: float):
        """Set the hysteresis value.

        Args:
            value: The hysteresis value to set.

        Returns:
            None
        """
        _LOGGER.debug("[%s] Setting hysteresis to %s", self._host, value)
        success = await self._async_try_command(
            "Error in set_hysteresis",
            self.coordinator.device.set_hysteresis,
            value,
        )
        if success:
            await asyncio.sleep(0.2)
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_hysteresis(self, hysteresis):
        """Set the hysteresis value (for service calls).

        Args:
            hysteresis: The hysteresis value to set.

        Returns:
            None
        """
        await self.async_set_native_value(hysteresis)

class HysenMaxTempNumber(HysenEntity, NumberEntity):
    """Representation of a Hysen Max Temperature number entity."""

    def __init__(self, device_data):
        """Initialize the number entity.

        Args:
            device_data: Dictionary containing device-specific data.
        """
        super().__init__(device_data["coordinator"], device_data)
        self._attr_unique_id = f"{device_data['mac']}_max_temp"
        self._attr_name = f"{device_data['name']} Max Temperature"
        self._attr_native_max_value = HYSENHEAT_MAX_TEMP
        self._attr_native_min_value = HYSENHEAT_MIN_TEMP
        self._attr_native_step = PRECISION_WHOLE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"
        self._attr_entity_registry_enabled_default = True

    @property
    def available(self):
        """Return True if the entity is available (not off mode).

        Returns:
            bool: Availability status.
        """
        power_state = self.coordinator.data.get(DATA_KEY_POWER_STATE)
        if not self.coordinator.last_update_success or power_state == STATE_OFF:
            _LOGGER.debug(
                "[%s] Max Temperature entity unavailable, power state: %s",
                self._host,
                power_state,
            )
            return False
        return True

    @property
    def native_value(self):
        """Return the current max temperature value based on HVAC mode.

        Returns:
            int: The current max temperature.
        """
        return self.coordinator.data.get(DATA_KEY_MAX_TEMP)

    async def async_set_native_value(self, value: float):
        """Set the max temperature value.

        Args:
            value: The max temperature to set.

        Returns:
            None

        Raises:
            ServiceValidationError: If the value is invalid for the current mode.
        """
        target_temp = self.coordinator.data.get(DATA_KEY_TARGET_TEMP)
        min_temp = self.coordinator.data.get(DATA_KEY_MIN_TEMP)
        if target_temp is not None and value < target_temp:
            _LOGGER.error(
                "[%s] Max temp (%s) cannot be set lower than target temp (%s)",
                self._host,
                value,
                target_temp,
            )
            raise ServiceValidationError(
                f"Max temperature ({value}°C) must not be lower than target temperature ({target_temp}°C)",
                translation_domain=DOMAIN,
                translation_key="missing_or_invalid_entity_id",
            )
        if min_temp is not None and value < min_temp:
            _LOGGER.error(
                "[%s] Max temp (%s) cannot be set lower than min temp (%s)",
                self._host,
                value,
                min_temp,
            )
            raise ServiceValidationError(
                f"Max temperature ({value}°C) must not be lower than min temperature ({min_temp}°C)",
                translation_domain=DOMAIN,
                translation_key="missing_or_invalid_entity_id",
            )
        _LOGGER.debug("[%s] Setting max temp to %s", self._host, value)
        success = await self._async_try_command(
            "Error in set_max_temp",
            self.coordinator.device.set_max_temp,
            int(value),
        )
        if success:
            await asyncio.sleep(0.2)
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_max_temp(self, max_temp):
        """Set the max temperature value (for service calls).

        Args:
            max_temp: The max temperature to set.

        Returns:
            None
        """
        await self.async_set_native_value(max_temp)

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        Returns:
            None
        """
        super()._handle_coordinator_update()
        self.async_write_ha_state()

class HysenMinTempNumber(HysenEntity, NumberEntity):
    """Representation of a Hysen Min Temperature number entity."""

    def __init__(self, device_data):
        """Initialize the number entity.

        Args:
            device_data: Dictionary containing device-specific data.
        """
        super().__init__(device_data["coordinator"], device_data)
        self._attr_unique_id = f"{device_data['mac']}_min_temp"
        self._attr_name = f"{device_data['name']} Min Temperature"
        self._attr_native_max_value = HYSENHEAT_MAX_TEMP
        self._attr_native_min_value = HYSENHEAT_MIN_TEMP
        self._attr_native_step = PRECISION_WHOLE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"
        self._attr_entity_registry_enabled_default = True

    @property
    def available(self):
        """Return True if the entity is available (not off mode).

        Returns:
            bool: Availability status.
        """
        power_state = self.coordinator.data.get(DATA_KEY_POWER_STATE)
        if not self.coordinator.last_update_success or power_state == STATE_OFF:
            _LOGGER.debug(
                "[%s] Min Temperature entity unavailable, power state: %s",
                self._host,
                power_state,
            )
            return False
        return True

    @property
    def native_value(self):
        """Return the current min temperature value based on HVAC mode.

        Returns:
            int: The current min temperature.
        """
        return self.coordinator.data.get(DATA_KEY_MIN_TEMP)

    async def async_set_native_value(self, value: float):
        """Set the min temperature value.

        Args:
            value: The min temperature to set.

        Returns:
            None

        Raises:
            ValueError: If the value is invalid for the current mode.
        """
        target_temp = self.coordinator.data.get(DATA_KEY_TARGET_TEMP)
        max_temp = self.coordinator.data.get(DATA_KEY_MAX_TEMP)
        if target_temp is not None and value > target_temp:
            _LOGGER.error(
                "[%s] Min temp (%s) cannot be set higher than target temp (%s)",
                self._host,
                value,
                target_temp,
            )
            raise ServiceValidationError(
                f"Min temperature ({value}°C) must not be higher than target temperature ({target_temp}°C)",
                translation_domain=DOMAIN,
                translation_key="missing_or_invalid_entity_id",
            )
        if max_temp is not None and value > max_temp:
            _LOGGER.error(
                "[%s] Min temp (%s) cannot be set higher than max temp (%s)",
                self._host,
                value,
                max_temp,
            )
            raise ServiceValidationError(
                f"Min temperature ({value}°C) must not be higher than max temperature ({max_temp}°C)",
                translation_domain=DOMAIN,
                translation_key="missing_or_invalid_entity_id",
            )
        _LOGGER.debug("[%s] Setting min temp to %s", self._host, value)
        success = await self._async_try_command(
            "Error in set_min_temp",
            self.coordinator.device.set_min_temp,
            int(value),
        )
        if success:
            await asyncio.sleep(0.2)
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_min_temp(self, min_temp):
        """Set the min temperature value (for service calls).

        Args:
            min_temp: The min temperature to set.

        Returns:
            None
        """
        await self.async_set_native_value(min_temp)

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        Returns:
            None
        """
        super()._handle_coordinator_update()
        self.async_write_ha_state()

class HysenCalibrationNumber(HysenEntity, NumberEntity):
    """Representation of a Hysen Calibration number entity."""

    def __init__(self, device_data):
        """Initialize the number entity.

        Args:
            device_data: Dictionary containing device-specific data.
        """
        super().__init__(device_data["coordinator"], device_data)
        self._attr_unique_id = f"{device_data['mac']}_calibration"
        self._attr_name = f"{device_data['name']} Sensor Calibration"
        self._attr_native_min_value = HYSENHEAT_CALIBRATION_MIN
        self._attr_native_max_value = HYSENHEAT_CALIBRATION_MAX
        self._attr_native_step = PRECISION_HALVES
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"

    @property
    def native_value(self):
        """Return the current calibration value.

        Returns:
            float: The current calibration.
        """
        return self.coordinator.data.get(DATA_KEY_CALIBRATION)

    async def async_set_native_value(self, value: float):
        """Set the calibration value.

        Args:
            value: The calibration value to set.

        Returns:
            None
        """
        _LOGGER.debug("[%s] Setting calibration to %s", self._host, value)
        success = await self._async_try_command(
            "Error in set_calibration",
            self.coordinator.device.set_calibration,
            value,
        )
        if success:
            await asyncio.sleep(0.2)
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_calibration(self, calibration):
        """Set the calibration value (for service calls).

        Args:
            calibration: The calibration value to set.

        Returns:
            None
        """
        await self.async_set_native_value(calibration)

class HysenSlotTempNumber(HysenEntity, NumberEntity):
    """Representation of a Hysen slot temperature number entity."""

    def __init__(self, device_data, slot: int, is_weekend: bool, data_key: str, service: str, service_attr: str, device_method: str):
        """Initialize the number entity.

        Args:
            device_data: Dictionary containing device-specific data.
            slot: The slot number (1-6 for weekdays, 1-2 for weekends).
            is_weekend: True if the slot is for a weekend, False for weekday.
            data_key: The key to retrieve the temperature value from coordinator.data.
            service: The service name for setting the temperature.
            service_attr: The attribute name for the service schema.
            device_method: The device method to call to set the temperature.
        """
        super().__init__(device_data["coordinator"], device_data)
        self._slot = slot
        self._is_weekend = is_weekend
        self._data_key = data_key
        self._service = service
        self._service_attr = service_attr
        self._device_method = device_method
        self._attr_unique_id = f"{device_data['mac']}_slot{slot}{'_we' if is_weekend else ''}_temp"
        self._attr_name = f"{device_data['name']} Slot {'We ' if is_weekend else ''}{slot} Temperature"
        self._attr_native_min_value = HYSENHEAT_DEFAULT_MIN_TEMP
        self._attr_native_max_value = HYSENHEAT_DEFAULT_MAX_TEMP
        self._attr_native_step = PRECISION_HALVES
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:thermometer"
        self._attr_entity_registry_enabled_default = True

    @property
    def native_value(self):
        """Return the current slot temperature.

        Returns:
            float: The current slot temperature, or None if unavailable.
        """
        value = self.coordinator.data.get(self._data_key)
        if value is None:
            _LOGGER.debug("[%s] No temperature value for %s", self._host, self._data_key)
            return None
        return float(value)

    async def async_set_native_value(self, value: float):
        """Set the slot temperature value.

        Args:
            value: The temperature to set.

        Returns:
            None
        """
        _LOGGER.debug("[%s] Setting slot %s%s temp to %s", self._host, self._slot, "_we" if self._is_weekend else "", value)
        operation_mode = self.coordinator.data.get(DATA_KEY_OPERATION_MODE)
        temporary_manual = self.coordinator.data.get(DATA_KEY_TEMPORARY_MANUAL)
        _LOGGER.debug("[%s] hvac mode: %s, temporary manual:%s", self._host, operation_mode, temporary_manual)
        success = await self._async_try_command(
            f"Error in {self._device_method}",
            getattr(self.coordinator.device, self._device_method),
            None,
            None,
            value,
        )
        if success:
            self.coordinator.data[self._data_key] = value
            if operation_mode == HVACMode.AUTO and temporary_manual == STATE_OFF:
                await self._async_try_command(
                    "Error in set_operation_mode",
                    self.coordinator.device.set_operation_mode,
                    MODE_HASS_TO_HYSEN[operation_mode],
                )
            await asyncio.sleep(0.2)
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_slot1_temp(self, slot1_temp: float):
        """Set the slot 1 temperature value (for service calls).

        Args:
            slot1_temp: The slot 1 temperature to set.

        Returns:
            None
        """
        await self.async_set_native_value(slot1_temp)

    async def async_set_slot2_temp(self, slot2_temp: float):
        """Set the slot 2 temperature value (for service calls).

        Args:
            slot2_temp: The slot 2 temperature to set.

        Returns:
            None
        """
        await self.async_set_native_value(slot2_temp)

    async def async_set_slot3_temp(self, slot3_temp: float):
        """Set the slot 3 temperature value (for service calls).

        Args:
            slot3_temp: The slot 3 temperature to set.

        Returns:
            None
        """
        await self.async_set_native_value(slot3_temp)

    async def async_set_slot4_temp(self, slot4_temp: float):
        """Set the slot 4 temperature value (for service calls).

        Args:
            slot4_temp: The slot 4 temperature to set.

        Returns:
            None
        """
        await self.async_set_native_value(slot4_temp)

    async def async_set_slot5_temp(self, slot5_temp: float):
        """Set the slot 5 temperature value (for service calls).

        Args:
            slot5_temp: The slot 5 temperature to set.

        Returns:
            None
        """
        await self.async_set_native_value(slot5_temp)

    async def async_set_slot6_temp(self, slot6_temp: float):
        """Set the slot 6 temperature value (for service calls).

        Args:
            slot6_temp: The slot 6 temperature to set.

        Returns:
            None
        """
        await self.async_set_native_value(slot6_temp)

    async def async_set_slot1_we_temp(self, slot1_we_temp: float):
        """Set the slot 1 weekend temperature value (for service calls).

        Args:
            slot1_we_temp: The slot 1 weekend temperature to set.

        Returns:
            None
        """
        await self.async_set_native_value(slot1_we_temp)

    async def async_set_slot2_we_temp(self, slot2_we_temp: float):
        """Set the slot 2 weekend temperature value (for service calls).

        Args:
            slot2_we_temp: The slot 2 weekend temperature to set.

        Returns:
            None
        """
        await self.async_set_native_value(slot2_we_temp)

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        Returns:
            None
        """
        super()._handle_coordinator_update()
        self.async_write_ha_state()
