from dataclasses import dataclass, field

from serde import serde

from servents.data_model.entity_types import (
    EntityType,
)

from servents.data_model.derived_consts import (
    BinarySensorDeviceClass,
    ButtonDeviceClass,
    EntityCategory,
    NumberDeviceClass,
    NumberMode,
    SensorDeviceClass,
    SensorStateClass,
    SwitchDeviceClass,
)

EntityID = str


@serde
@dataclass(kw_only=True)
class DeviceConfig:
    device_id: str
    name: str
    manufacturer: str | None = None
    model: str | None = None
    version: str | None = None
    app_name: str | None = None
    is_global: bool = False


@serde
@dataclass(kw_only=True)
class EntityConfig:
    entity_type: EntityType
    servent_id: str
    name: str
    default_state: str | bool | int | float | None = None
    fixed_attributes: dict[str, str | bool | int | float] = field(default_factory=dict)
    entity_category: EntityCategory | None = None
    disabled_by_default: bool = False
    app_name: str | None = None
    device_definition: DeviceConfig | None = None


@serde
@dataclass(kw_only=True)
class SensorConfig(EntityConfig):
    entity_type: EntityType = EntityType.SENSOR
    device_class: SensorDeviceClass | None = None
    unit_of_measurement: str | None = None
    state_class: SensorStateClass | None = None
    options: list[str] | None = None
    entity_ids: list[EntityID] | None = None

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
