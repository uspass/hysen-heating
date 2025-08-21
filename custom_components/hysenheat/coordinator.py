"""
DataUpdateCoordinator for Hysen Heating integration.
"""

import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from .const import (
    DOMAIN,
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
#    DATA_KEY_SLOT1_OFF,
    DATA_KEY_UNKNOWN2,
    DATA_KEY_UNKNOWN3,
    STATE_ON,
    STATE_OFF,
    KEY_LOCK_HYSEN_TO_HASS,
    TEMPORARY_MANUAL_HYSEN_TO_HASS,
    VALVE_STATE_HYSEN_TO_HASS,
    POWER_STATE_HYSEN_TO_HASS,
    MODE_HYSEN_TO_HASS,
    PRESET_HYSEN_TO_HASS,
    SENSOR_TYPE_HYSEN_TO_HASS,
    FROST_PROTECTION_HYSEN_TO_HASS,
    POWERON_HYSEN_TO_HASS,
)

_LOGGER = logging.getLogger(__name__)

class HysenCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Hysen device data.

    Periodically updates device status and maps it to Home Assistant-compatible formats.
    """

    def __init__(self, hass: HomeAssistant, device, host):
        """Initialize the Hysen coordinator.

        Args:
            hass: The Home Assistant instance.
            device: The HysenHeatingDevice instance to communicate with.
            host: The host address of the device.
        """
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{host}",
            update_interval=timedelta(seconds=30),
        )
        self.device = device
        self.host = host

    async def _async_update_data(self):
        """Fetch data from the Hysen device.

        Retrieves the latest device status and maps it to Home Assistant-compatible formats.

        Returns:
            dict: A dictionary containing the updated device data.

        Raises:
            UpdateFailed: If communication with the device fails.
        """
        _LOGGER.debug("Fetching data for device at %s", self.host)
        try:
            await self.hass.async_add_executor_job(self.device.get_device_status)
            data = {
                DATA_KEY_FWVERSION: self.device.fwversion,
                DATA_KEY_KEY_LOCK: KEY_LOCK_HYSEN_TO_HASS.get(self.device.key_lock),
                DATA_KEY_TEMPORARY_MANUAL: TEMPORARY_MANUAL_HYSEN_TO_HASS.get(self.device.manual_in_auto),
                DATA_KEY_VALVE_STATE: VALVE_STATE_HYSEN_TO_HASS.get(self.device.valve_state),
                DATA_KEY_POWER_STATE: POWER_STATE_HYSEN_TO_HASS.get(self.device.power_state),
                DATA_KEY_ROOM_TEMP: self.device.room_temp,
                DATA_KEY_TARGET_TEMP: self.device.target_temp,
                DATA_KEY_OPERATION_MODE: MODE_HYSEN_TO_HASS.get(self.device.operation_mode),
                DATA_KEY_PRESET_MODE: PRESET_HYSEN_TO_HASS.get(self.device.schedule),
                DATA_KEY_SENSOR_TYPE: SENSOR_TYPE_HYSEN_TO_HASS.get(self.device.sensor),
                DATA_KEY_EXTERNAL_MAX_TEMP: self.device.external_max_temp,
                DATA_KEY_HYSTERESIS: self.device.hysteresis,
                DATA_KEY_MAX_TEMP: self.device.max_temp,
                DATA_KEY_MIN_TEMP: self.device.min_temp,
                DATA_KEY_CALIBRATION: self.device.calibration,
                DATA_KEY_FROST_PROTECTION: FROST_PROTECTION_HYSEN_TO_HASS.get(self.device.frost_protection),
                DATA_KEY_POWERON: POWERON_HYSEN_TO_HASS.get(self.device.poweron),
                DATA_KEY_UNKNOWN1: self.device.unknown1,
                DATA_KEY_EXTERNAL_TEMP: self.device.external_temp,
                DATA_KEY_CLOCK_HOUR: self.device.clock_hour,
                DATA_KEY_CLOCK_MINUTE: self.device.clock_minute,
                DATA_KEY_CLOCK_SECOND: self.device.clock_second,
                DATA_KEY_CLOCK_WEEKDAY: self.device.clock_weekday,
                DATA_KEY_SLOT1_TIME: f"{self.device.period1_hour}:{self.device.period1_min:02d}",
                DATA_KEY_SLOT2_TIME: f"{self.device.period2_hour}:{self.device.period2_min:02d}",
                DATA_KEY_SLOT3_TIME: f"{self.device.period3_hour}:{self.device.period3_min:02d}",
                DATA_KEY_SLOT4_TIME: f"{self.device.period4_hour}:{self.device.period4_min:02d}",
                DATA_KEY_SLOT5_TIME: f"{self.device.period5_hour}:{self.device.period5_min:02d}",
                DATA_KEY_SLOT6_TIME: f"{self.device.period6_hour}:{self.device.period6_min:02d}",
                DATA_KEY_SLOT1_WE_TIME:  f"{self.device.we_period1_hour}:{self.device.we_period1_min:02d}",
                DATA_KEY_SLOT2_WE_TIME:  f"{self.device.we_period2_hour}:{self.device.we_period2_min:02d}",
                DATA_KEY_SLOT1_TEMP: self.device.period1_temp,
                DATA_KEY_SLOT2_TEMP: self.device.period2_temp,
                DATA_KEY_SLOT3_TEMP: self.device.period3_temp,
                DATA_KEY_SLOT4_TEMP: self.device.period4_temp,
                DATA_KEY_SLOT5_TEMP: self.device.period5_temp,
                DATA_KEY_SLOT6_TEMP: self.device.period6_temp,
                DATA_KEY_SLOT1_WE_TEMP: self.device.we_period1_temp,
                DATA_KEY_SLOT2_WE_TEMP: self.device.we_period2_temp,
#                DATA_KEY_SLOT1_OFF: STATE_ON if self.device.period1_temp == 0.0 else STATE_OFF,
#                DATA_KEY_SLOT1_OFF: STATE_ON,
                DATA_KEY_UNKNOWN2: self.device.unknown2,
                DATA_KEY_UNKNOWN3: self.device.unknown3,
            }
            _LOGGER.debug("Updated coordinator data for %s: %s", self.host, data)
            return data
        except Exception as exc:
            _LOGGER.error("Failed to update device data for %s: %s", self.host, exc)
            raise UpdateFailed(f"Error communicating with device: {exc}") from exc