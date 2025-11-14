import pytest
from serde.json import from_json, to_json

from servents.data_model.entity_configs import SensorConfig
from servents.data_model.entity_types import EntityType


class TestSensorConfig:
    def test_sensor_config_minimal(self):
        config = SensorConfig(
            servent_id="test_servent",
            name="Test Sensor",
        )

        json_str = to_json(config)
        deserialized = from_json(SensorConfig, json_str)

        assert deserialized.entity_type == EntityType.SENSOR
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.device_class is None
        assert deserialized.unit_of_measurement is None
        assert deserialized.state_class is None
        assert deserialized.options is None

    def test_sensor_config_with_device_class(self):
        config = SensorConfig(
            servent_id="test_servent",
            name="Temperature Sensor",
            device_class="temperature",
            unit_of_measurement="°C",
            state_class="measurement",
        )

        json_str = to_json(config)
        deserialized = from_json(SensorConfig, json_str)

        assert deserialized.device_class == "temperature"
        assert deserialized.unit_of_measurement == "°C"
        assert deserialized.state_class == "measurement"

    def test_sensor_config_enum_with_options(self):
        config = SensorConfig(
            servent_id="test_servent",
            name="Mode Selector",
            options=["mode1", "mode2", "mode3"],
        )

        json_str = to_json(config)
        deserialized = from_json(SensorConfig, json_str)

        assert deserialized.device_class == "enum"
        assert deserialized.options is not None
        assert list(deserialized.options) == ["mode1", "mode2", "mode3"]

    def test_sensor_config_enum_explicit(self):
        config = SensorConfig(
            servent_id="test_servent",
            name="Mode Selector",
            device_class="enum",
            options=["mode1", "mode2", "mode3"],
        )

        json_str = to_json(config)
        deserialized = from_json(SensorConfig, json_str)

        assert deserialized.device_class == "enum"
        assert deserialized.options is not None
        assert list(deserialized.options) == ["mode1", "mode2", "mode3"]

    def test_sensor_config_invalid_options_without_enum(self):
        with pytest.raises(ValueError, match="device class should be `enum`"):
            SensorConfig(
                servent_id="test_servent",
                name="Test Sensor",
                device_class="temperature",
                options=["option1", "option2"],
            )

    def test_sensor_config_full(self):
        config = SensorConfig(
            servent_id="test_servent",
            name="Test Sensor",
            default_state=25.5,
            fixed_attributes={"precision": 0.1},
            entity_category="diagnostic",
            disabled_by_default=False,
            app_name="test_app",
            device_class="temperature",
            unit_of_measurement="°C",
            state_class="measurement",
        )

        json_str = to_json(config)
        deserialized = from_json(SensorConfig, json_str)

        assert deserialized.entity_type == EntityType.SENSOR
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.default_state == config.default_state
        assert deserialized.fixed_attributes == config.fixed_attributes
        assert deserialized.entity_category == config.entity_category
        assert deserialized.disabled_by_default == config.disabled_by_default
        assert deserialized.app_name == config.app_name
        assert deserialized.device_class == config.device_class
        assert deserialized.unit_of_measurement == config.unit_of_measurement
        assert deserialized.state_class == config.state_class
