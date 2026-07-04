import pytest
from serde import SerdeError, from_dict
from serde.json import from_json, to_json

from servents.data_model.entity_configs import (
    ClimateConfig,
    CoverConfig,
    DateConfig,
    DatetimeConfig,
    EventConfig,
    FanConfig,
    LightConfig,
    LockConfig,
    SirenConfig,
    TextConfig,
    TimeConfig,
    ValveConfig,
)
from servents.data_model.entity_types import EntityType


BASE_DEVICE = {
    "device_id": "test-device",
    "name": "Test Device",
    "manufacturer": "ServEnts",
    "model": "Live Harness",
    "version": "Domovoy",
    "suggested_area": "Kitchen",
    "configuration_url": "https://example.test/config",
    "sw_version": "1.2.3",
    "hw_version": "rev-a",
    "serial_number": "serial-123",
}


def payload(entity_type: str, **extra):
    return {
        "entity_type": entity_type,
        "servent_id": f"test-{entity_type}",
        "name": f"Test {entity_type}",
        "default_state": extra.pop("default_state", None),
        "fixed_attributes": {"phase": 1},
        "disabled_by_default": False,
        "restore_state": False,
        "previous_servent_ids": [f"old-test-{entity_type}"],
        "app_name": "test_app",
        "device_definition": BASE_DEVICE,
        **extra,
    }


ROUND_TRIP_CASES = [
    (
        LightConfig,
        payload("light", default_state={"state": True, "brightness": 128}, supports_brightness=True, optimistic=True),
    ),
    (
        CoverConfig,
        payload(
            "cover",
            default_state={"state": "open", "position": 100},
            device_class="garage",
            supports_position=True,
            supports_stop=True,
            optimistic=True,
        ),
    ),
    (
        FanConfig,
        payload(
            "fan",
            default_state={"state": True, "percentage": 50},
            supports_percentage=True,
            preset_modes=["eco", "boost"],
            optimistic=True,
        ),
    ),
    (
        ClimateConfig,
        payload(
            "climate",
            default_state="off",
            hvac_modes=["off", "heat", "cool"],
            supports_target_temperature=True,
            supports_target_temperature_range=False,
            min_temp=15,
            max_temp=25,
            temp_step=0.5,
            fan_modes=["auto", "high"],
            preset_modes=["eco"],
            swing_modes=["off", "on"],
            temperature_unit="C",
            optimistic=True,
        ),
    ),
    (
        LockConfig,
        payload("lock", default_state="locked", supports_open=True, code_format="^\\d{4}$", optimistic=True),
    ),
    (
        ValveConfig,
        payload(
            "valve",
            default_state={"state": "closed", "position": 0},
            device_class="water",
            supports_position=True,
            supports_stop=True,
            optimistic=True,
        ),
    ),
    (
        SirenConfig,
        payload(
            "siren",
            default_state=False,
            available_tones=["fire", "warning"],
            supports_volume_set=True,
            supports_duration=True,
            optimistic=True,
        ),
    ),
    (
        TextConfig,
        payload("text", default_state="hello", min_length=1, max_length=100, pattern="^[a-z]+$", mode="text"),
    ),
    (DateConfig, payload("date", default_state="2026-07-04")),
    (TimeConfig, payload("time", default_state="12:30:00")),
    (DatetimeConfig, payload("date_time", default_state="2026-07-04T12:30:00+00:00")),
    (
        EventConfig,
        payload("event", event_types=["pressed", "held"], device_class="doorbell"),
    ),
]


class TestWorkOrderConfigs:
    @pytest.mark.parametrize(("config_type", "config_payload"), ROUND_TRIP_CASES)
    def test_work_order_payload_roundtrip(self, config_type, config_payload):
        config = from_dict(config_type, config_payload)
        json_str = to_json(config)
        deserialized = from_json(config_type, json_str)

        assert deserialized.entity_type.value == config_payload["entity_type"]
        assert deserialized.servent_id == config_payload["servent_id"]
        assert deserialized.name == config_payload["name"]
        assert deserialized.default_state == config_payload["default_state"]
        assert deserialized.restore_state is False
        assert deserialized.previous_servent_ids == config_payload["previous_servent_ids"]
        assert deserialized.device_definition is not None
        assert deserialized.device_definition.sw_version == "1.2.3"

    def test_entity_type_wire_values(self):
        assert EntityType.LIGHT.value == "light"
        assert EntityType.COVER.value == "cover"
        assert EntityType.FAN.value == "fan"
        assert EntityType.CLIMATE.value == "climate"
        assert EntityType.LOCK.value == "lock"
        assert EntityType.VALVE.value == "valve"
        assert EntityType.SIREN.value == "siren"
        assert EntityType.TEXT.value == "text"
        assert EntityType.DATE.value == "date"
        assert EntityType.TIME.value == "time"
        assert EntityType.DATETIME.value == "date_time"
        assert EntityType.EVENT.value == "event"

    def test_climate_rejects_invalid_target_temperature_flags(self):
        with pytest.raises(ValueError, match="Exactly one"):
            ClimateConfig(
                servent_id="climate",
                name="Climate",
                supports_target_temperature=True,
                supports_target_temperature_range=True,
            )

        with pytest.raises(ValueError, match="Exactly one"):
            ClimateConfig(
                servent_id="climate",
                name="Climate",
                supports_target_temperature=False,
                supports_target_temperature_range=False,
            )

    def test_climate_rejects_invalid_modes_and_bounds(self):
        with pytest.raises(ValueError, match="hvac_modes"):
            ClimateConfig(servent_id="climate", name="Climate", hvac_modes=["off", "invalid"])

        with pytest.raises(ValueError, match="must include 'off'"):
            ClimateConfig(servent_id="climate", name="Climate", hvac_modes=["heat"])

        with pytest.raises(ValueError, match="max_temp"):
            ClimateConfig(servent_id="climate", name="Climate", min_temp=25, max_temp=20)

        with pytest.raises((SerdeError, ValueError), match="temperature_unit"):
            ClimateConfig(servent_id="climate", name="Climate", temperature_unit="K")  # type: ignore[arg-type]

    def test_text_rejects_invalid_bounds_and_mode(self):
        with pytest.raises((SerdeError, ValueError), match="mode"):
            TextConfig(servent_id="text", name="Text", mode="secret")  # type: ignore[arg-type]

        with pytest.raises(ValueError, match="min_length"):
            TextConfig(servent_id="text", name="Text", min_length=-1)

        with pytest.raises(ValueError, match="max_length"):
            TextConfig(servent_id="text", name="Text", min_length=10, max_length=5)

    def test_event_rejects_empty_event_types_and_invalid_device_class(self):
        with pytest.raises(ValueError, match="event_types"):
            EventConfig(servent_id="event", name="Event", event_types=[])

        with pytest.raises((SerdeError, ValueError), match="device_class"):
            EventConfig(
                servent_id="event",
                name="Event",
                event_types=["pressed"],
                device_class="noise",  # type: ignore[arg-type]
            )

    def test_device_class_literals(self):
        with pytest.raises((SerdeError, ValueError), match="device_class"):
            CoverConfig(servent_id="cover", name="Cover", device_class="roof")  # type: ignore[arg-type]

        with pytest.raises((SerdeError, ValueError), match="device_class"):
            ValveConfig(servent_id="valve", name="Valve", device_class="oil")  # type: ignore[arg-type]
