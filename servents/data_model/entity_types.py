from enum import StrEnum


class EntityType(StrEnum):
    BINARY_SENSOR = "binary_sensor"
    BUTTON = "button"
    CLIMATE = "climate"
    COVER = "cover"
    DATE = "date"
    DATETIME = "date_time"
    EVENT = "event"
    FAN = "fan"
    LIGHT = "light"
    LOCK = "lock"
    NUMBER = "number"
    SELECT = "select"
    SENSOR = "sensor"
    SIREN = "siren"
    SWITCH = "switch"
    TEXT = "text"
    THRESHOLD_BINARY_SENSOR = "threshold"
    TIME = "time"
    VALVE = "valve"
