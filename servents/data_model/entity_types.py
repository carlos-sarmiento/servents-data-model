from enum import StrEnum


class EntityType(StrEnum):
    BINARY_SENSOR = "binary_sensor"
    BUTTON = "button"
    NUMBER = "number"
    SELECT = "select"
    SENSOR = "sensor"
    SWITCH = "switch"
    THRESHOLD_BINARY_SENSOR = "threshold"
