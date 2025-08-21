"""
Support for Hysen Heating Controller.

This module provides a climate entity for controlling the Hysen HY03WE Wifi
device and derivatives, supporting HVAC modes, temperature settings,
and advanced features like scheduling.
"""

import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.exceptions import ServiceValidationError
from datetime import datetime
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_platform
from homeassistant.components.climate import ClimateEntity, ClimateEntityFeature
from .const import (
    DOMAIN,
    ATTR_ENTITY_ID,
    ATTR_TEMPERATURE,
    PRECISION_WHOLE,
    PRECISION_HALVES,
    UnitOfTemperature,
    DEFAULT_CURRENT_TEMP,
    DEFAULT_TARGET_TEMP,
    DEFAULT_MIN_TEMP,
    DEFAULT_MAX_TEMP,
    DEFAULT_CALIBRATION,
    DATA_KEY_FWVERSION,
    DATA_KEY_KEY_LOCK,
    DATA_KEY_TEMPORARY_MANUAL,
    DATA_KEY_VALVE_STATE,
    DATA_KEY_POWER_STATE,
    DATA_KEY_ROOM_TEMP,
    DATA_KEY_TARGET_TEMP,
    DATA_KEY_OPERATION_MODE,
    DATA_KEY_PRESET_MODE,
    DATA_KEY_SENSOR_TYPE,
    DATA_KEY_EXTERNAL_MAX_TEMP,
    DATA_KEY_HYSTERESIS,
    DATA_KEY_MAX_TEMP,
    DATA_KEY_MIN_TEMP,
    DATA_KEY_CALIBRATION,
    DATA_KEY_FROST_PROTECTION,
    DATA_KEY_POWERON,
    DATA_KEY_UNKNOWN1,
    DATA_KEY_EXTERNAL_TEMP,
    DATA_KEY_CLOCK_HOUR,
    DATA_KEY_CLOCK_MINUTE,
    DATA_KEY_CLOCK_SECOND,
    DATA_KEY_CLOCK_WEEKDAY,
    DATA_KEY_SLOT1_TIME,
    DATA_KEY_SLOT2_TIME,
    DATA_KEY_SLOT3_TIME,
    DATA_KEY_SLOT4_TIME,
    DATA_KEY_SLOT5_TIME,
    DATA_KEY_SLOT6_TIME,
    DATA_KEY_SLOT1_WE_TIME,
    DATA_KEY_SLOT2_WE_TIME,
    DATA_KEY_SLOT1_TEMP,
    DATA_KEY_SLOT2_TEMP,
    DATA_KEY_SLOT3_TEMP,
    DATA_KEY_SLOT4_TEMP,
    DATA_KEY_SLOT5_TEMP,
    DATA_KEY_SLOT6_TEMP,
    DATA_KEY_SLOT1_WE_TEMP,
    DATA_KEY_SLOT2_WE_TEMP,
    DATA_KEY_UNKNOWN2,
    DATA_KEY_UNKNOWN3,
    STATE_ON,
    STATE_OFF,
    STATE_CLOSED,
    STATE_SENSOR_INTERNAL,
    STATE_SENSOR_EXTERNAL,
    HVACMode,
    HVACAction,
    ATTR_HVAC_MODE,
    ATTR_PRESET_MODE,
    ATTR_PRESET_MODES,
    ATTR_OPERATION_MODE,
    ATTR_FWVERSION,
    ATTR_KEY_LOCK,
    ATTR_TEMPORARY_MANUAL,
    ATTR_VALVE_STATE,
    ATTR_POWER_STATE,
    ATTR_ROOM_TEMP,
    ATTR_SENSOR_TYPE,
    ATTR_EXTERNAL_MAX_TEMP,
    ATTR_HYSTERESIS,
    ATTR_MAX_TEMP,
    ATTR_MIN_TEMP,
    ATTR_CALIBRATION,
    ATTR_FROST_PROTECTION,
    ATTR_POWERON,
    ATTR_UNKNOWN1,
    ATTR_EXTERNAL_TEMP,
    ATTR_DEVICE_TIME,
    ATTR_DEVICE_WEEKDAY,
    ATTR_SLOT1_TIME,
    ATTR_SLOT2_TIME,
    ATTR_SLOT3_TIME,
    ATTR_SLOT4_TIME,
    ATTR_SLOT5_TIME,
    ATTR_SLOT6_TIME,
    ATTR_SLOT1_WE_TIME,
    ATTR_SLOT2_WE_TIME,
    ATTR_SLOT1_TEMP,
    ATTR_SLOT2_TEMP,
    ATTR_SLOT3_TEMP,
    ATTR_SLOT4_TEMP,
    ATTR_SLOT5_TEMP,
    ATTR_SLOT6_TEMP,
    ATTR_SLOT1_WE_TEMP,
    ATTR_SLOT2_WE_TEMP,
    ATTR_UNKNOWN2,
    ATTR_UNKNOWN3,
    SERVICE_TURN_ON,
    SERVICE_TURN_OFF,
    HVAC_MODES,
    PRESET_TEMPORARY,
    PRESET_WORKDAYS,
    PRESET_SIXDAYS,
    PRESET_FULLWEEK,
    PRESET_MODES,
    PRESET_MODES_TEMPORARY,
    POWER_STATE_HASS_TO_HYSEN,
    MODE_HASS_TO_HYSEN,
    PRESET_HASS_TO_HYSEN,
)
from .entity import HysenEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up the Hysen climate entity from a config entry.

    Args:
        hass (HomeAssistant): The Home Assistant instance.
        config_entry: The configuration entry for the device.
        async_add_entities: Callback to add entities to Home Assistant.
    """
    device_data = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([HysenClimate(device_data)])

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_TURN_ON,
        {},
        "async_turn_on",
    )
    platform.async_register_entity_service(
        SERVICE_TURN_OFF,
        {},
        "async_turn_off",
    )

class HysenClimate(HysenEntity, ClimateEntity):
    """Representation of a Hysen Heating climate entity.

    This class, inheriting from HysenEntity and ClimateEntity, manages the state
    and control of a Hysen climate device, supporting HVAC modes, temperature
    settings, and scheduling.
    """

    def __init__(self, device_data):
        """Initialize the climate entity.

        Args:
            device_data (dict): Configuration data for the device, including coordinator, mac, name, and host.
        """
        super().__init__(device_data["coordinator"], device_data)
        self._attr_unique_id = f"{device_data['mac']}_climate"
        self._attr_name = device_data["name"]
        self._attr_precision = PRECISION_HALVES
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_target_temperature_step = PRECISION_HALVES
        self._attr_power_state = self.coordinator.data.get(DATA_KEY_POWER_STATE)
        self._attr_operation_mode = self.coordinator.data.get(DATA_KEY_OPERATION_MODE)
        self._attr_temporary_manual = self.coordinator.data.get(DATA_KEY_TEMPORARY_MANUAL)
        self._attr_hvac_mode = None
        self._attr_hvac_modes = HVAC_MODES
        self._attr_preset_modes = PRESET_MODES
        self._attr_preset_mode = None
        self._attr_valve_state = self.coordinator.data.get(DATA_KEY_VALVE_STATE)
        self._attr_sensor_type = self.coordinator.data.get(DATA_KEY_SENSOR_TYPE)
        self._attr_min_temp = self.coordinator.data.get(DATA_KEY_MIN_TEMP)
        self._attr_max_temp = self.coordinator.data.get(DATA_KEY_MAX_TEMP)
        self._host = device_data["host"]

    @property
    def supported_features(self):
        """Return the list of supported features.

        Returns:
            int: A bitwise combination of supported ClimateEntityFeature flags.
        """
        if self._attr_power_state == STATE_OFF or self._attr_hvac_mode == HVACMode.OFF:
            self._attr_supported_features = (
                ClimateEntityFeature.TURN_ON
                | ClimateEntityFeature.TURN_OFF
            )
        elif self._attr_hvac_mode == HVACMode.HEAT and self._attr_temporary_manual == STATE_OFF:
            self._attr_supported_features = (
                ClimateEntityFeature.TURN_ON
                | ClimateEntityFeature.TURN_OFF
                | ClimateEntityFeature.TARGET_TEMPERATURE
            )
        else:  # hvac_mode is HEAT (temporary) or AUTO
            self._attr_supported_features = (
                ClimateEntityFeature.TURN_ON
                | ClimateEntityFeature.TURN_OFF
                | ClimateEntityFeature.TARGET_TEMPERATURE
                | ClimateEntityFeature.PRESET_MODE
            )
        return self._attr_supported_features

    @property
    def precision(self):
        """Return the precision of the system.

        Returns:
            float: The precision for temperature settings (e.g., whole numbers).
        """
        return self._attr_precision

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses.

        Returns:
            str: The temperature unit, e.g., UnitOfTemperature.CELSIUS.
        """
        return self._attr_temperature_unit

    @property
    def hvac_mode(self):
        """Return the current HVAC mode.

        Returns:
            str: The current HVAC mode.
        """
        return self._attr_hvac_mode

    @property
    def hvac_modes(self):
        """Return the list of available HVAC modes.

        Returns:
            list: The list of supported HVAC modes, dynamically adjusted based on state.
        """
        return self._attr_hvac_modes

    @property
    def hvac_action(self):
        """Return the current HVAC action.

        Returns:
            str: The current HVAC action (e.g., off, heating, idle).
        """
        if self._attr_power_state == STATE_OFF:
            self._attr_hvac_action = HVACAction.OFF
        elif self._attr_hvac_mode is None:
            _LOGGER.warning("[%s] Unknown operation mode: %s", self._host, self._attr_hvac_mode)
            self._attr_hvac_action = HVACAction.IDLE  # Default to IDLE for safety
        elif self._attr_valve_state is None:
            _LOGGER.warning("[%s] Unknown valve state: %s", self._host, self._attr_valve_state)
            self._attr_hvac_action = HVACAction.IDLE  # Default to IDLE for safety
        elif self._attr_valve_state == STATE_CLOSED:
            self._attr_hvac_action = HVACAction.IDLE
        else:
            self._attr_hvac_action = HVACAction.HEATING
        return self._attr_hvac_action

    @property
    def current_temperature(self):
        """Return the current temperature.

        Returns:
            float: The current room temperature from the device.
        """
        return self._attr_current_temperature

    @property
    def target_temperature(self):
        """Return the target temperature.

        Returns:
            float: The current target temperature.
        """
        if self._attr_power_state == STATE_ON:
            return self._attr_target_temperature
        return None

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature.

        Returns:
            float: The step for adjusting target temperature.
        """
        return self._attr_target_temperature_step

    @property
    def min_temp(self):
        """Return the minimum temperature.

        Returns:
            float: The minimum temperature setting supported by the device.
        """
        return self._attr_min_temp

    @property
    def max_temp(self):
        """Return the maximum temperature.

        Returns:
            float: The maximum temperature setting supported by the device.
        """
        return self._attr_max_temp

    @property
    def preset_mode(self):
        """Return the preset mode.

        Returns:
            str: The current preset mode.
        """
        return self._attr_preset_mode

    @property
    def preset_modes(self):
        """Return the list of available preset modes.

        Returns:
            list: The list of supported preset modes.
        """
        return self._attr_preset_modes

    @property
    def power_state(self):
        """Return the power state.

        Returns:
            str: The current power state (on or off).
        """
        return self._attr_power_state

    @property
    def operation_mode(self):
        """Return the operation mode.

        Returns:
            str: The current operation mode (heat or auto).
        """
        return self._attr_operation_mode

    @property
    def valve_state(self):
        """Return the valve state.

        Returns:
            str: The current valve state (open or closed).
        """
        return self._attr_valve_state

    @property
    def sensor_type(self):
        """Return the sensor type.

        Returns:
            str: The current sensor type (internal, external or internal with external maximum).
        """
        return self._attr_sensor_type

    @property
    def temporary_manual(self):
        """Return the manual in auto.

        Returns:
            str: The current manual in auto (false or true).
        """
        return self._attr_temporary_manual

    @property
    def extra_state_attributes(self):
        """Return the state attributes.

        Returns:
            dict: Additional state attributes for the entity.
        """
        data = {
            ATTR_POWER_STATE: self._attr_power_state,
            ATTR_OPERATION_MODE: self._attr_operation_mode,
            ATTR_TEMPORARY_MANUAL: self._attr_temporary_manual,
            ATTR_HVAC_MODE: self._attr_hvac_mode,
            ATTR_PRESET_MODE: self._attr_preset_mode,
            ATTR_PRESET_MODES: self._attr_preset_modes,
            ATTR_VALVE_STATE: self._attr_valve_state,
            ATTR_KEY_LOCK: self.coordinator.data.get(DATA_KEY_KEY_LOCK),
            ATTR_SENSOR_TYPE: self._attr_sensor_type,
            ATTR_ROOM_TEMP: self.coordinator.data.get(DATA_KEY_ROOM_TEMP),
            ATTR_EXTERNAL_TEMP: self.coordinator.data.get(DATA_KEY_EXTERNAL_TEMP),
            ATTR_EXTERNAL_MAX_TEMP: self.coordinator.data.get(DATA_KEY_EXTERNAL_MAX_TEMP),
            ATTR_HYSTERESIS: self.coordinator.data.get(DATA_KEY_HYSTERESIS),
            ATTR_CALIBRATION: self.coordinator.data.get(DATA_KEY_CALIBRATION),
            ATTR_FROST_PROTECTION: self.coordinator.data.get(DATA_KEY_FROST_PROTECTION),
            ATTR_POWERON: self.coordinator.data.get(DATA_KEY_POWERON),
            ATTR_UNKNOWN1: self.coordinator.data.get(DATA_KEY_UNKNOWN1),
            ATTR_DEVICE_TIME: f"{self.coordinator.data.get(DATA_KEY_CLOCK_HOUR)}:{self.coordinator.data.get(DATA_KEY_CLOCK_MINUTE):02d}",
            ATTR_DEVICE_WEEKDAY: self.coordinator.data.get(DATA_KEY_CLOCK_WEEKDAY),
            ATTR_SLOT1_TIME: self.coordinator.data.get(DATA_KEY_SLOT1_TIME),
            ATTR_SLOT1_TEMP: self.coordinator.data.get(DATA_KEY_SLOT1_TEMP),
            ATTR_SLOT2_TIME: self.coordinator.data.get(DATA_KEY_SLOT2_TIME),
            ATTR_SLOT2_TEMP: self.coordinator.data.get(DATA_KEY_SLOT2_TEMP),
            ATTR_SLOT3_TIME: self.coordinator.data.get(DATA_KEY_SLOT3_TIME),
            ATTR_SLOT3_TEMP: self.coordinator.data.get(DATA_KEY_SLOT3_TEMP),
            ATTR_SLOT4_TIME: self.coordinator.data.get(DATA_KEY_SLOT4_TIME),
            ATTR_SLOT4_TEMP: self.coordinator.data.get(DATA_KEY_SLOT4_TEMP),
            ATTR_SLOT5_TIME: self.coordinator.data.get(DATA_KEY_SLOT5_TIME),
            ATTR_SLOT5_TEMP: self.coordinator.data.get(DATA_KEY_SLOT5_TEMP),
            ATTR_SLOT6_TIME: self.coordinator.data.get(DATA_KEY_SLOT6_TIME),
            ATTR_SLOT6_TEMP: self.coordinator.data.get(DATA_KEY_SLOT6_TEMP),
            ATTR_SLOT1_WE_TIME: self.coordinator.data.get(DATA_KEY_SLOT1_WE_TIME),
            ATTR_SLOT1_WE_TEMP: self.coordinator.data.get(DATA_KEY_SLOT1_WE_TEMP),
            ATTR_SLOT2_WE_TIME: self.coordinator.data.get(DATA_KEY_SLOT2_WE_TIME),
            ATTR_SLOT2_WE_TEMP: self.coordinator.data.get(DATA_KEY_SLOT2_WE_TEMP),
            ATTR_FWVERSION: self.coordinator.data.get(DATA_KEY_FWVERSION),
            ATTR_UNKNOWN2: self.coordinator.data.get(DATA_KEY_UNKNOWN2),
            ATTR_UNKNOWN3: self.coordinator.data.get(DATA_KEY_UNKNOWN3),
        }
        return {k: v for k, v in data.items() if v is not None}

    async def async_turn_on(self):
        """Turn the entity on.

        Sends a command to power on the device and refreshes the state.
        """
        _LOGGER.debug("Hytemp: [%s] Turning on", self._host)
        success = await self._async_try_command(
            "Error in set_power",
            self.coordinator.device.set_power,
            POWER_STATE_HASS_TO_HYSEN[STATE_ON],
        )
        if success:
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_turn_off(self):
        """Turn the entity off.

        Sends a command to power off the device and refreshes the state.
        """
        _LOGGER.debug("Hytemp: [%s] Turning off", self._host)
        success = await self._async_try_command(
            "Error in set_power",
            self.coordinator.device.set_power,
            POWER_STATE_HASS_TO_HYSEN[STATE_OFF],
        )
        if success:
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature.

        Args:
            **kwargs: Keyword arguments containing the target temperature (ATTR_TEMPERATURE).

        Notes:
            If ATTR_TEMPERATURE is not provided, the method does nothing.
            Setting a temperature in AUTO mode triggers temporary manual mode, updating preset mode to temporary.
        """
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        _LOGGER.debug("Hytemp: [%s] Setting target temperature to %s", self._host, temperature)
        success = await self._async_try_command(
            "Error in set_target_temp",
            self.coordinator.device.set_target_temp,
            temperature,
        )
        if success and self._attr_hvac_mode == HVACMode.AUTO:
            # In AUTO mode, setting temperature triggers temporary manual mode
            self._attr_preset_mode = PRESET_TEMPORARY
            self._attr_preset_modes = PRESET_MODES_TEMPORARY
        if success:
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        """Set the HVAC mode.

        Args:
            hvac_mode (str): The desired HVAC mode (e.g., HEAT, AUTO, OFF).

        Raises:
            ServiceValidationError: If the provided hvac_mode is not valid.
        """
        _LOGGER.debug("Hytemp: [%s] HVAC modes are %s", self._host, self._attr_hvac_modes)
        _LOGGER.debug("Hytemp: [%s] Requested HVAC mode is %s", self._host, hvac_mode)
        valid_modes = HVAC_MODES
        if hvac_mode not in valid_modes:
            _LOGGER.error("Hytemp: [%s] HVAC mode %s is not valid. Valid HVAC modes are: %s", self._host, hvac_mode, ", ".join(valid_modes))
            raise ServiceValidationError(
                f"Hytemp: Invalid HVAC mode: {hvac_mode}. Valid modes are: {valid_modes}.",
                translation_domain=DOMAIN,
                translation_key="invalid_hvac_mode",
            )
        _LOGGER.debug("Hytemp: [%s] Setting HVAC mode to %s", self._host, hvac_mode)
        success = True
        if hvac_mode == HVACMode.OFF:
            # Power off the device
            success = await self._async_try_command(
                "Error in set_power",
                self.coordinator.device.set_power,
                POWER_STATE_HASS_TO_HYSEN[STATE_OFF],
            )
        else:
            if self._attr_power_state == STATE_OFF:
                # Turn on the device if it's off
                success = await self._async_try_command(
                    "Error in set_power",
                    self.coordinator.device.set_power,
                    POWER_STATE_HASS_TO_HYSEN[STATE_ON],
                )
            if success:
                # Set the selected HVAC mode
                success = await self._async_try_command(
                    "Error in set_operation_mode",
                    self.coordinator.device.set_operation_mode,
                    MODE_HASS_TO_HYSEN[hvac_mode],
                )
            if success and hvac_mode == HVACMode.AUTO:# and self._attr_temporary_manual == STATE_ON:
                # Setting AUTO when temporary_manual is ON resets to schedule-based preset
                self._attr_preset_modes = PRESET_MODES
                self._attr_preset_mode = self.coordinator.data.get(DATA_KEY_PRESET_MODE)
        if success:
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_set_preset_mode(self, preset_mode):
        """Set the preset mode.

        Args:
            preset_mode (str): The desired preset mode (e.g., workdays, sixdays, full week).

        Raises:
            ServiceValidationError: If the provided preset_mode is not valid or is PRESET_TEMPORARY.

        Notes:
            Only schedule-based preset modes (workdays, sixdays, full week) can be set.
            The temporary preset mode is automatically set when the target temperature is changed in AUTO mode.
        """
        _LOGGER.debug("Hytemp: [%s] Setting preset mode to %s", self._host, preset_mode)
        valid_modes = self._attr_preset_modes
        if preset_mode not in valid_modes:
            _LOGGER.error("Hytemp: [%s] Preset mode %s is not valid. Valid preset modes are: %s", self._host, preset_mode, ", ".join(valid_modes))
            raise ServiceValidationError(
                f"Hytemp: Invalid preset mode: {preset_mode}. Valid modes are: {valid_modes}.",
                translation_domain=DOMAIN,
                translation_key="invalid_preset_mode",
            )
        if preset_mode == PRESET_TEMPORARY:
            _LOGGER.error("Hytemp: [%s] Cannot set preset mode to temporary manually", self._host)
            raise ServiceValidationError(
                "Hytemp: Cannot set preset mode to temporary manually. It is set automatically when changing the target temperature in AUTO mode.",
                translation_domain=DOMAIN,
                translation_key="invalid_preset_mode",
            )
        # Set weekly schedule for schedule-based preset modes
        success = await self._async_try_command(
            "Error in set_weekly_schedule",
            self.coordinator.device.set_weekly_schedule,
            PRESET_HASS_TO_HYSEN[preset_mode],
        )
        # Set preset attributes to reflect the new schedule
        if success:
            self._attr_preset_mode = preset_mode
            self._attr_preset_modes = PRESET_MODES
            await self.coordinator.async_refresh()
            self.async_write_ha_state()

    async def async_added_to_hass(self):
        """Initialize the entity when added to Home Assistant.

        Calls the parent method and triggers an initial state update.
        """
        await super().async_added_to_hass()
        await self.async_update()

    async def async_update(self):
        """Update the entity state from the coordinator data.

        Updates attributes such as power state, HVAC mode, temperatures, and preset modes.
        """
        self._attr_power_state = self.coordinator.data.get(DATA_KEY_POWER_STATE)
        self._attr_temporary_manual = self.coordinator.data.get(DATA_KEY_TEMPORARY_MANUAL)
        self._attr_operation_mode = self.coordinator.data.get(DATA_KEY_OPERATION_MODE)
        self._attr_hvac_mode = (
            HVACMode.OFF if self._attr_power_state == STATE_OFF
            else HVACMode.HEAT if self._attr_temporary_manual == STATE_ON
            else self._attr_operation_mode
        )
        self._attr_preset_mode = (
            PRESET_TEMPORARY if self._attr_temporary_manual == STATE_ON
            else self.coordinator.data.get(DATA_KEY_PRESET_MODE)
        )
        self._attr_preset_modes = (
            PRESET_MODES_TEMPORARY if self._attr_temporary_manual == STATE_ON
            else PRESET_MODES
        )
        self._attr_current_temperature = (
            self.coordinator.data.get(DATA_KEY_EXTERNAL_TEMP)
            if self._attr_sensor_type == STATE_SENSOR_EXTERNAL
            else self.coordinator.data.get(DATA_KEY_ROOM_TEMP)
        )
        self._attr_target_temperature = self.coordinator.data.get(DATA_KEY_TARGET_TEMP)
        self._attr_min_temp = self.coordinator.data.get(DATA_KEY_MIN_TEMP)
        self._attr_max_temp = self.coordinator.data.get(DATA_KEY_MAX_TEMP)
        self._attr_valve_state = self.coordinator.data.get(DATA_KEY_VALVE_STATE)
        self._attr_sensor_type = self.coordinator.data.get(DATA_KEY_SENSOR_TYPE)
        self.async_write_ha_state()
