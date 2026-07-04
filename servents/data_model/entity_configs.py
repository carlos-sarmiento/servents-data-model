from dataclasses import dataclass, field
from typing import Any, get_args

from serde import serde

from servents.data_model.entity_types import (
    EntityType,
)

from servents.data_model.derived_consts import (
    BinarySensorDeviceClass,
    ButtonDeviceClass,
    ClimateHVACMode,
    ClimateTemperatureUnit,
    CoverDeviceClass,
    EntityCategory,
    EventDeviceClass,
    NumberDeviceClass,
    NumberMode,
    SensorDeviceClass,
    SensorStateClass,
    SwitchDeviceClass,
    TextMode,
    ValveDeviceClass,
)

EntityID = str


def _validate_literal(value: Any, literal_type: Any, field_name: str) -> None:
    if value is None:
        return

    allowed = get_args(literal_type)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}; got {value!r}")


def _validate_literal_list(
    values: list[str] | None,
    literal_type: Any,
    field_name: str,
    *,
    allow_empty: bool = True,
) -> None:
    if values is None:
        return
    if not values and not allow_empty:
        raise ValueError(f"{field_name} must not be empty")

    allowed = get_args(literal_type)
    invalid = [value for value in values if value not in allowed]
    if invalid:
        raise ValueError(f"{field_name} must contain only {allowed}; got {invalid!r}")


@serde
@dataclass(kw_only=True)
class DeviceConfig:
    device_id: str
    name: str
    manufacturer: str | None = None
    model: str | None = None
    version: str | None = None
    suggested_area: str | None = None
    configuration_url: str | None = None
    sw_version: str | None = None
    hw_version: str | None = None
    serial_number: str | None = None
    app_name: str | None = None
    is_global: bool = False


@serde
@dataclass(kw_only=True)
class EntityConfig:
    entity_type: EntityType
    servent_id: str
    name: str
    default_state: Any | None = None
    fixed_attributes: dict[str, Any] = field(default_factory=dict)
    entity_category: EntityCategory | None = None
    disabled_by_default: bool = False
    restore_state: bool = True
    previous_servent_ids: list[str] | None = None
    app_name: str | None = None
    device_definition: DeviceConfig | None = None


@serde
@dataclass(kw_only=True)
class LightConfig(EntityConfig):
    entity_type: EntityType = EntityType.LIGHT
    supports_brightness: bool = False
    optimistic: bool = False


@serde
@dataclass(kw_only=True)
class CoverConfig(EntityConfig):
    entity_type: EntityType = EntityType.COVER
    device_class: CoverDeviceClass | None = None
    supports_position: bool = False
    supports_stop: bool = False
    optimistic: bool = False

    def __post_init__(self) -> None:
        _validate_literal(self.device_class, CoverDeviceClass, "device_class")


@serde
@dataclass(kw_only=True)
class FanConfig(EntityConfig):
    entity_type: EntityType = EntityType.FAN
    supports_percentage: bool = False
    preset_modes: list[str] | None = None
    optimistic: bool = False


@serde
@dataclass(kw_only=True)
class ClimateConfig(EntityConfig):
    entity_type: EntityType = EntityType.CLIMATE
    hvac_modes: list[str] | None = None
    supports_target_temperature: bool = True
    supports_target_temperature_range: bool = False
    min_temp: float | int | None = None
    max_temp: float | int | None = None
    temp_step: float | int | None = None
    fan_modes: list[str] | None = None
    preset_modes: list[str] | None = None
    swing_modes: list[str] | None = None
    temperature_unit: ClimateTemperatureUnit = "C"  # pyright: ignore[reportGeneralTypeIssues]
    optimistic: bool = False

    def __post_init__(self) -> None:
        if self.supports_target_temperature == self.supports_target_temperature_range:
            raise ValueError(
                "Exactly one of supports_target_temperature and "
                "supports_target_temperature_range must be true"
            )

        _validate_literal_list(self.hvac_modes, ClimateHVACMode, "hvac_modes")
        if self.hvac_modes is not None and "off" not in self.hvac_modes:
            raise ValueError("hvac_modes must include 'off'")

        if self.min_temp is not None and self.max_temp is not None and self.max_temp <= self.min_temp:
            raise ValueError("max_temp must be greater than min_temp")

        _validate_literal(self.temperature_unit, ClimateTemperatureUnit, "temperature_unit")


@serde
@dataclass(kw_only=True)
class LockConfig(EntityConfig):
    entity_type: EntityType = EntityType.LOCK
    supports_open: bool = False
    code_format: str | None = None
    optimistic: bool = False


@serde
@dataclass(kw_only=True)
class ValveConfig(EntityConfig):
    entity_type: EntityType = EntityType.VALVE
    device_class: ValveDeviceClass | None = None
    supports_position: bool = False
    supports_stop: bool = False
    optimistic: bool = False

    def __post_init__(self) -> None:
        _validate_literal(self.device_class, ValveDeviceClass, "device_class")


@serde
@dataclass(kw_only=True)
class SirenConfig(EntityConfig):
    entity_type: EntityType = EntityType.SIREN
    available_tones: list[str] | None = None
    supports_volume_set: bool = False
    supports_duration: bool = False
    optimistic: bool = False


@serde
@dataclass(kw_only=True)
class TextConfig(EntityConfig):
    entity_type: EntityType = EntityType.TEXT
    min_length: int | None = None
    max_length: int | None = None
    pattern: str | None = None
    mode: TextMode = "text"  # pyright: ignore[reportGeneralTypeIssues]

    def __post_init__(self) -> None:
        _validate_literal(self.mode, TextMode, "mode")

        if self.min_length is not None and self.min_length < 0:
            raise ValueError("min_length must be greater than or equal to 0")
        if self.max_length is not None and self.max_length < 0:
            raise ValueError("max_length must be greater than or equal to 0")
        if self.min_length is not None and self.max_length is not None and self.max_length < self.min_length:
            raise ValueError("max_length must be greater than or equal to min_length")


@serde
@dataclass(kw_only=True)
class DateConfig(EntityConfig):
    entity_type: EntityType = EntityType.DATE


@serde
@dataclass(kw_only=True)
class TimeConfig(EntityConfig):
    entity_type: EntityType = EntityType.TIME


@serde
@dataclass(kw_only=True)
class DatetimeConfig(EntityConfig):
    entity_type: EntityType = EntityType.DATETIME


@serde
@dataclass(kw_only=True)
class EventConfig(EntityConfig):
    entity_type: EntityType = EntityType.EVENT
    event_types: list[str]  # pyright: ignore[reportGeneralTypeIssues]
    device_class: EventDeviceClass | None = None

    def __post_init__(self) -> None:
        if not self.event_types:
            raise ValueError("event_types must not be empty")
        _validate_literal(self.device_class, EventDeviceClass, "device_class")


@serde
@dataclass(kw_only=True)
class SensorConfig(EntityConfig):
    entity_type: EntityType = EntityType.SENSOR
    device_class: SensorDeviceClass | None = None
    unit_of_measurement: str | None = None
    state_class: SensorStateClass | None = None
    options: list[str] | None = None

    def __post_init__(self) -> None:
        if self.options is not None and self.device_class is None:
            self.device_class = "enum"

        elif self.options is not None and self.device_class != "enum":
            raise ValueError(
                "If providing Options for a sensor, the device class should be `enum`",
            )
        else:
            self.device_class = self.device_class


@serde
@dataclass(kw_only=True)
class NumberConfig(EntityConfig):
    entity_type: EntityType = EntityType.NUMBER
    device_class: NumberDeviceClass | None = None
    unit_of_measurement: str | None = None
    mode: NumberMode  # pyright: ignore[reportGeneralTypeIssues]
    min_value: float | int | None = None
    max_value: float | int | None = None
    step: float | int | None = None


@serde
@dataclass(kw_only=True)
class BinarySensorConfig(EntityConfig):
    entity_type: EntityType = EntityType.BINARY_SENSOR
    device_class: BinarySensorDeviceClass | None = None

    def __post_init__(self) -> None:
        if self.entity_category == "config":
            raise ValueError(
                "Binary sensors cannot have the 'config' entity category.",
            )


@serde
@dataclass(kw_only=True)
class ThresholdBinarySensorConfig(EntityConfig):
    entity_type: EntityType = EntityType.THRESHOLD_BINARY_SENSOR
    entity_id: EntityID  # pyright: ignore[reportGeneralTypeIssues]
    device_class: BinarySensorDeviceClass | None = None
    lower: float | int | None = None
    upper: float | int | None = None
    hysteresis: float | int = 0

    def __post_init__(self) -> None:
        if self.lower is None and self.upper is None:
            raise ValueError(
                "Threshold sensor must have at least a lower or an upper value set.",
            )


@serde
@dataclass(kw_only=True)
class SelectConfig(EntityConfig):
    entity_type: EntityType = EntityType.SELECT
    options: list[str]  # pyright: ignore[reportGeneralTypeIssues]


@serde
@dataclass(kw_only=True)
class SwitchConfig(EntityConfig):
    entity_type: EntityType = EntityType.SWITCH
    device_class: SwitchDeviceClass | None = None


@serde
@dataclass(kw_only=True)
class ButtonConfig(EntityConfig):
    entity_type: EntityType = EntityType.BUTTON
    event: str  # pyright: ignore[reportGeneralTypeIssues]
    event_data: dict = field(default_factory=dict)
    device_class: ButtonDeviceClass | None = None
