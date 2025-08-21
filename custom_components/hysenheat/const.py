"""Constants for the Hysen Heating Coil Controller integration."""

from hysen import (
    HysenHeatingDevice,
    HYSENHEAT_KEY_LOCK_OFF,
    HYSENHEAT_KEY_LOCK_ON,
    HYSENHEAT_MANUAL_IN_AUTO_OFF,
    HYSENHEAT_MANUAL_IN_AUTO_ON,
    HYSENHEAT_POWER_OFF,
    HYSENHEAT_POWER_ON,
    HYSENHEAT_VALVE_OFF,
    HYSENHEAT_VALVE_ON,
    HYSENHEAT_MODE_MANUAL,
    HYSENHEAT_MODE_AUTO,
    HYSENHEAT_SCHEDULE_12345_67,
    HYSENHEAT_SCHEDULE_123456_7,
    HYSENHEAT_SCHEDULE_1234567,
    HYSENHEAT_SENSOR_INTERNAL,
    HYSENHEAT_SENSOR_EXTERNAL,
    HYSENHEAT_SENSOR_INT_EXT,
    HYSENHEAT_HYSTERESIS_MIN,
    HYSENHEAT_HYSTERESIS_MAX,
    HYSENHEAT_MAX_TEMP,
    HYSENHEAT_MIN_TEMP,
    HYSENHEAT_CALIBRATION_MIN,
    HYSENHEAT_CALIBRATION_MAX,
    HYSENHEAT_FROST_PROTECTION_OFF,
    HYSENHEAT_FROST_PROTECTION_ON,
    HYSENHEAT_POWERON_OFF,
    HYSENHEAT_POWERON_ON,
    HYSENHEAT_WEEKDAY_MONDAY,
    HYSENHEAT_WEEKDAY_SUNDAY,
)
from homeassistant.const import (
    Platform,
    CONF_HOST, 
    CONF_MAC, 
    CONF_NAME, 
    CONF_TIMEOUT,
    ATTR_ENTITY_ID,
    ATTR_TEMPERATURE,
    PRECISION_WHOLE,
    PRECISION_HALVES,
    UnitOfTemperature,    
    UnitOfTime,
)
from homeassistant.components.climate.const import (
    ATTR_HVAC_MODE,
    ATTR_PRESET_MODE,
    ATTR_PRESET_MODES,
    HVACMode,
    HVACAction,
)

# Integration domain
DOMAIN = "hysenheat"

# Platforms supported
PLATFORMS = [
#    Platform.BINARY_SENSOR, 
    Platform.BUTTON, 
    Platform.CLIMATE, 
    Platform.NUMBER, 
    Platform.SELECT, 
    Platform.SENSOR, 
    Platform.SWITCH, 
    Platform.TIME
]

# Configuration keys
CONF_SYNC_CLOCK = "sync_clock"
CONF_SYNC_HOUR = "sync_hour"

# Default values
DEFAULT_NAME = "Hysen Heating"
DEFAULT_TIMEOUT = 10
DEFAULT_SYNC_CLOCK = False
DEFAULT_SYNC_HOUR = 4
DEFAULT_CURRENT_TEMP = 22
DEFAULT_TARGET_TEMP = 22
DEFAULT_MIN_TEMP = 5
DEFAULT_MAX_TEMP = 99
DEFAULT_EXTERNAL_MAX_TEMP = 99
DEFAULT_CALIBRATION = 0
HYSENHEAT_DEFAULT_MAX_TEMP = 35
HYSENHEAT_DEFAULT_MIN_TEMP = 5

# Data keys for coordinator
DATA_KEY_FWVERSION = "fwversion"
DATA_KEY_KEY_LOCK = "key_lock"
DATA_KEY_TEMPORARY_MANUAL = "temporary_manual"
DATA_KEY_VALVE_STATE = "valve_state"
DATA_KEY_POWER_STATE = "power_state"
DATA_KEY_ROOM_TEMP = "room_temp"
DATA_KEY_TARGET_TEMP = "target_temp"
DATA_KEY_OPERATION_MODE = "operation_mode"
DATA_KEY_PRESET_MODE = "schedule"
DATA_KEY_SENSOR_TYPE = "sensor"
DATA_KEY_EXTERNAL_MAX_TEMP = "external_max_temp"
DATA_KEY_HYSTERESIS = "hysteresis"
DATA_KEY_MAX_TEMP = "max_temp"
DATA_KEY_MIN_TEMP = "min_temp"
DATA_KEY_CALIBRATION = "calibration"
DATA_KEY_FROST_PROTECTION = "frost_protection"
DATA_KEY_POWERON = "poweron"
DATA_KEY_UNKNOWN1 = "unknown1"
DATA_KEY_EXTERNAL_TEMP = "external_temp"
DATA_KEY_CLOCK_HOUR = "clock_hour"
DATA_KEY_CLOCK_MINUTE = "clock_minute"
DATA_KEY_CLOCK_SECOND = "clock_second"
DATA_KEY_CLOCK_WEEKDAY = "clock_weekday"
DATA_KEY_SLOT1_TIME = "period1_time"
DATA_KEY_SLOT2_TIME = "period2_time"
DATA_KEY_SLOT3_TIME = "period3_time"
DATA_KEY_SLOT4_TIME = "period4_time"
DATA_KEY_SLOT5_TIME = "period5_time"
DATA_KEY_SLOT6_TIME = "period6_time"
DATA_KEY_SLOT1_WE_TIME = "we_period1_time"
DATA_KEY_SLOT2_WE_TIME = "we_period2_time"
DATA_KEY_SLOT1_TEMP = "period1_temp"
DATA_KEY_SLOT2_TEMP = "period2_temp"
DATA_KEY_SLOT3_TEMP = "period3_temp"
DATA_KEY_SLOT4_TEMP = "period4_temp"
DATA_KEY_SLOT5_TEMP = "period5_temp"
DATA_KEY_SLOT6_TEMP = "period6_temp"
DATA_KEY_SLOT1_WE_TEMP = "we_period1_temp"
DATA_KEY_SLOT2_WE_TEMP = "we_period2_temp"
DATA_KEY_SLOT1_OFF = "period1_off"
DATA_KEY_UNKNOWN2 = "unknown2"
DATA_KEY_UNKNOWN3 = "unknown3"

# State values
STATE_ON = "on"
STATE_OFF = "off"
STATE_OPEN = "open"
STATE_CLOSED = "closed"
STATE_UNLOCKED = "Unlocked"
STATE_LOCKED = "Locked"
STATE_SENSOR_INTERNAL   = "Internal"
STATE_SENSOR_EXTERNAL   = "External"
STATE_SENSOR_INT_EXT    = "IntControl_ExternalLimit"

# HVAC modes
HVAC_MODES = [HVACMode.OFF, HVACMode.HEAT, HVACMode.AUTO]

# Preset values
PRESET_TEMPORARY = "Temporary"
PRESET_WORKDAYS = "Workdays"
PRESET_SIXDAYS = "Sixdays"
PRESET_FULLWEEK = "Fullweek"

# Preset modes
PRESET_MODES_TEMPORARY = [PRESET_TEMPORARY]
PRESET_MODES = [PRESET_WORKDAYS, PRESET_SIXDAYS, PRESET_FULLWEEK]

# Attribute names
ATTR_FWVERSION = "firmware_version"
ATTR_KEY_LOCK = "key_lock"
ATTR_TEMPORARY_MANUAL = "temporary_manual"
ATTR_VALVE_STATE = "valve_state"
ATTR_POWER_STATE = "power_state"
ATTR_OPERATION_MODE = "operation_mode"
ATTR_ROOM_TEMP = "room_temp"
ATTR_SENSOR_TYPE = "sensor_type"
ATTR_EXTERNAL_MAX_TEMP = "external_max_temp"
ATTR_HYSTERESIS = "hysteresis"
ATTR_MAX_TEMP = "max_temp"
ATTR_MIN_TEMP = "min_temp"
ATTR_CALIBRATION = "calibration"
ATTR_FROST_PROTECTION = "frost_protection"
ATTR_POWERON = "poweron"
ATTR_UNKNOWN1 = "unknown1"
ATTR_EXTERNAL_TEMP = "external_temp"
ATTR_DEVICE_TIME = "time_now"
ATTR_DEVICE_WEEKDAY = "device_weekday"
ATTR_SLOT1_TIME = "slot1_time"
ATTR_SLOT2_TIME = "slot2_time"
ATTR_SLOT3_TIME = "slot3_time"
ATTR_SLOT4_TIME = "slot4_time"
ATTR_SLOT5_TIME = "slot5_time"
ATTR_SLOT6_TIME = "slot6_time"
ATTR_SLOT1_WE_TIME = "slot1_we_time"
ATTR_SLOT2_WE_TIME = "slot2_we_time"
ATTR_SLOT1_TEMP = "slot1_temp"
ATTR_SLOT2_TEMP = "slot2_temp"
ATTR_SLOT3_TEMP = "slot3_temp"
ATTR_SLOT4_TEMP = "slot4_temp"
ATTR_SLOT5_TEMP = "slot5_temp"
ATTR_SLOT6_TEMP = "slot6_temp"
ATTR_SLOT1_WE_TEMP = "slot1_we_temp"
ATTR_SLOT2_WE_TEMP = "slot2_we_temp"
ATTR_SLOT1_OFF = "slot1_off"
ATTR_UNKNOWN2 = "unknown2"
ATTR_UNKNOWN3 = "unknown3"

# Service names
SERVICE_TURN_ON = "turn_on"
SERVICE_TURN_OFF = "turn_off"
SERVICE_SET_HVAC_MODE = "set_hvac_mode"
SERVICE_SET_TEMPERATURE = "set_temperature"
SERVICE_SET_PRESET_MODE = "set_preset_mode"
SERVICE_SET_KEY_LOCK = "set_key_lock"
SERVICE_SET_SENSOR_TYPE = 'set_sensor_type'
SERVICE_SET_EXTERNAL_MAX_TEMP = 'set_external_max_temp'
SERVICE_SET_HYSTERESIS = "set_hysteresis"
SERVICE_SET_MAX_TEMP = "set_max_temp"
SERVICE_SET_MIN_TEMP = "set_min_temp"
SERVICE_SET_CALIBRATION = "set_calibration"
SERVICE_SET_FROST_PROTECTION = "set_frost_protection"
SERVICE_SET_POWERON = 'set_poweron'
SERVICE_SET_TIME = "set_time"
SERVICE_SET_SLOT1_TIME = "set_slot1_time"
SERVICE_SET_SLOT2_TIME = "set_slot2_time"
SERVICE_SET_SLOT3_TIME = "set_slot3_time"
SERVICE_SET_SLOT4_TIME = "set_slot4_time"
SERVICE_SET_SLOT5_TIME = "set_slot5_time"
SERVICE_SET_SLOT6_TIME = "set_slot6_time"
SERVICE_SET_SLOT1_WE_TIME = "set_slot1_we_time"
SERVICE_SET_SLOT2_WE_TIME = "set_slot2_we_time"
SERVICE_SET_SLOT1_TEMP = "set_slot1_temp"
SERVICE_SET_SLOT2_TEMP = "set_slot2_temp"
SERVICE_SET_SLOT3_TEMP = "set_slot3_temp"
SERVICE_SET_SLOT4_TEMP = "set_slot4_temp"
SERVICE_SET_SLOT5_TEMP = "set_slot5_temp"
SERVICE_SET_SLOT6_TEMP = "set_slot6_temp"
SERVICE_SET_SLOT1_WE_TEMP = "set_slot1_we_temp"
SERVICE_SET_SLOT2_WE_TEMP = "set_slot2_we_temp"
SERVICE_SET_SLOT1_OFF = "set_slot1_off"

# Mappings
KEY_LOCK_HYSEN_TO_HASS = {
    HYSENHEAT_KEY_LOCK_OFF : STATE_UNLOCKED,
    HYSENHEAT_KEY_LOCK_ON  : STATE_LOCKED,
}
KEY_LOCK_HASS_TO_HYSEN = {v: k for k, v in KEY_LOCK_HYSEN_TO_HASS.items()}

TEMPORARY_MANUAL_HYSEN_TO_HASS = {
    HYSENHEAT_MANUAL_IN_AUTO_ON  : STATE_ON,
    HYSENHEAT_MANUAL_IN_AUTO_OFF : STATE_OFF,
}

VALVE_STATE_HYSEN_TO_HASS = {
    HYSENHEAT_VALVE_ON  : STATE_OPEN,
    HYSENHEAT_VALVE_OFF : STATE_CLOSED,
}

POWER_STATE_HYSEN_TO_HASS = {
    HYSENHEAT_POWER_ON  : STATE_ON,
    HYSENHEAT_POWER_OFF : STATE_OFF,
}
POWER_STATE_HASS_TO_HYSEN = {v: k for k, v in POWER_STATE_HYSEN_TO_HASS.items()}

MODE_HYSEN_TO_HASS = {
    HYSENHEAT_MODE_MANUAL: HVACMode.HEAT,
    HYSENHEAT_MODE_AUTO: HVACMode.AUTO,
}
MODE_HASS_TO_HYSEN = {v: k for k, v in MODE_HYSEN_TO_HASS.items()}

PRESET_HYSEN_TO_HASS = {
    HYSENHEAT_SCHEDULE_12345_67 : PRESET_WORKDAYS,
    HYSENHEAT_SCHEDULE_123456_7 : PRESET_SIXDAYS,
    HYSENHEAT_SCHEDULE_1234567  : PRESET_FULLWEEK,
}
PRESET_HASS_TO_HYSEN = {v: k for k, v in PRESET_HYSEN_TO_HASS.items()}

SENSOR_TYPE_HYSEN_TO_HASS = {
    HYSENHEAT_SENSOR_INTERNAL : STATE_SENSOR_INTERNAL,
    HYSENHEAT_SENSOR_EXTERNAL : STATE_SENSOR_EXTERNAL,
    HYSENHEAT_SENSOR_INT_EXT : STATE_SENSOR_INT_EXT,
}
SENSOR_TYPE_HASS_TO_HYSEN = {v: k for k, v in SENSOR_TYPE_HYSEN_TO_HASS.items()}

FROST_PROTECTION_HYSEN_TO_HASS = {
    HYSENHEAT_FROST_PROTECTION_ON  : STATE_ON,
    HYSENHEAT_FROST_PROTECTION_OFF : STATE_OFF,
}
FROST_PROTECTION_HASS_TO_HYSEN = {v: k for k, v in FROST_PROTECTION_HYSEN_TO_HASS.items()}

POWERON_HYSEN_TO_HASS = {
    HYSENHEAT_POWERON_ON  : STATE_ON,
    HYSENHEAT_POWERON_OFF : STATE_OFF,
}
POWERON_HASS_TO_HYSEN = {v: k for k, v in POWERON_HYSEN_TO_HASS.items()}

