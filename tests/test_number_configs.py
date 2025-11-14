from serde.json import from_json, to_json

from servents.data_model.entity_configs import NumberConfig
from servents.data_model.entity_types import EntityType


class TestNumberConfig:
    def test_number_config_minimal(self):
        config = NumberConfig(
            servent_id="test_servent",
            name="Test Number",
            mode="slider",
        )

        json_str = to_json(config)
        deserialized = from_json(NumberConfig, json_str)

        assert deserialized.entity_type == EntityType.NUMBER
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.mode == "slider"
        assert deserialized.device_class is None
        assert deserialized.unit_of_measurement is None
        assert deserialized.min_value is None
        assert deserialized.max_value is None
        assert deserialized.step is None

    def test_number_config_full(self):
        config = NumberConfig(
            servent_id="test_servent",
            name="Test Number",
            mode="box",
            device_class="temperature",
            unit_of_measurement="°C",
            min_value=0.0,
            max_value=100.0,
            step=0.5,
            default_state=20.0,
            entity_category="config",
        )

        json_str = to_json(config)
        deserialized = from_json(NumberConfig, json_str)

        assert deserialized.entity_type == EntityType.NUMBER
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.mode == config.mode
        assert deserialized.device_class == config.device_class
        assert deserialized.unit_of_measurement == config.unit_of_measurement
        assert deserialized.min_value == config.min_value
        assert deserialized.max_value == config.max_value
        assert deserialized.step == config.step
        assert deserialized.default_state == config.default_state
        assert deserialized.entity_category == config.entity_category

    def test_number_config_modes(self):
        modes = ["auto", "box", "slider"]
        for mode in modes:
            config = NumberConfig(
                servent_id="test_servent",
                name="Test Number",
                mode=mode,  # type: ignore
            )

            json_str = to_json(config)
            deserialized = from_json(NumberConfig, json_str)

            assert deserialized.mode == mode
