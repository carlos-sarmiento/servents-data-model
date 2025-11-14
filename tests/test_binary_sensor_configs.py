import pytest
from serde.json import from_json, to_json

from servents.data_model.entity_configs import (
    BinarySensorConfig,
    ThresholdBinarySensorConfig,
)
from servents.data_model.entity_types import EntityType


class TestBinarySensorConfig:
    def test_binary_sensor_config_minimal(self):
        config = BinarySensorConfig(
            servent_id="test_servent",
            name="Test Binary Sensor",
        )

        json_str = to_json(config)
        deserialized = from_json(BinarySensorConfig, json_str)

        assert deserialized.entity_type == EntityType.BINARY_SENSOR
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.device_class is None

    def test_binary_sensor_config_with_device_class(self):
        config = BinarySensorConfig(
            servent_id="test_servent",
            name="Motion Sensor",
            device_class="motion",
        )

        json_str = to_json(config)
        deserialized = from_json(BinarySensorConfig, json_str)

        assert deserialized.device_class == "motion"

    def test_binary_sensor_config_full(self):
        config = BinarySensorConfig(
            servent_id="test_servent",
            name="Test Binary Sensor",
            device_class="occupancy",
            default_state=False,
            entity_category="diagnostic",
            disabled_by_default=True,
        )

        json_str = to_json(config)
        deserialized = from_json(BinarySensorConfig, json_str)

        assert deserialized.entity_type == EntityType.BINARY_SENSOR
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.device_class == config.device_class
        assert deserialized.default_state == config.default_state
        assert deserialized.entity_category == config.entity_category
        assert deserialized.disabled_by_default == config.disabled_by_default


class TestThresholdBinarySensorConfig:
    def test_threshold_binary_sensor_with_lower(self):
        config = ThresholdBinarySensorConfig(
            servent_id="test_servent",
            name="Low Threshold Sensor",
            entity_id="sensor.temperature",
            lower=10.0,
        )

        json_str = to_json(config)
        deserialized = from_json(ThresholdBinarySensorConfig, json_str)

        assert deserialized.entity_type == EntityType.THRESHOLD_BINARY_SENSOR
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.entity_id == config.entity_id
        assert deserialized.lower == config.lower
        assert deserialized.upper is None
        assert deserialized.hysteresis == 0.0

    def test_threshold_binary_sensor_with_upper(self):
        config = ThresholdBinarySensorConfig(
            servent_id="test_servent",
            name="High Threshold Sensor",
            entity_id="sensor.temperature",
            upper=30.0,
        )

        json_str = to_json(config)
        deserialized = from_json(ThresholdBinarySensorConfig, json_str)

        assert deserialized.entity_id == config.entity_id
        assert deserialized.lower is None
        assert deserialized.upper == config.upper
        assert deserialized.hysteresis == 0.0 or deserialized.hysteresis == 0

    def test_threshold_binary_sensor_with_both(self):
        config = ThresholdBinarySensorConfig(
            servent_id="test_servent",
            name="Range Threshold Sensor",
            entity_id="sensor.temperature",
            lower=10.0,
            upper=30.0,
            hysteresis=2.0,
        )

        json_str = to_json(config)
        deserialized = from_json(ThresholdBinarySensorConfig, json_str)

        assert deserialized.entity_id == config.entity_id
        assert deserialized.lower == config.lower
        assert deserialized.upper == config.upper
        assert deserialized.hysteresis == config.hysteresis

    def test_threshold_binary_sensor_invalid_no_thresholds(self):
        with pytest.raises(ValueError, match="must have at least a lower or an upper"):
            ThresholdBinarySensorConfig(
                servent_id="test_servent",
                name="Invalid Sensor",
                entity_id="sensor.temperature",
            )

    def test_threshold_binary_sensor_full(self):
        config = ThresholdBinarySensorConfig(
            servent_id="test_servent",
            name="Test Threshold Sensor",
            entity_id="sensor.temperature",
            device_class="cold",
            lower=5.0,
            upper=15.0,
            hysteresis=1.0,
            default_state=False,
            entity_category="diagnostic",
        )

        json_str = to_json(config)
        deserialized = from_json(ThresholdBinarySensorConfig, json_str)

        assert deserialized.entity_type == EntityType.THRESHOLD_BINARY_SENSOR
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.entity_id == config.entity_id
        assert deserialized.device_class == config.device_class
        assert deserialized.lower == config.lower
        assert deserialized.upper == config.upper
        assert deserialized.hysteresis == config.hysteresis
        assert deserialized.default_state == config.default_state
        assert deserialized.entity_category == config.entity_category
