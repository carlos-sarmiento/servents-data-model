from serde.json import from_json, to_json

from servents.data_model.entity_configs import (
    ButtonConfig,
)
from servents.data_model.entity_types import EntityType


class TestButtonConfig:
    def test_button_config_minimal(self):
        config = ButtonConfig(
            servent_id="test_servent",
            name="Test Button",
            event="test_event",
        )

        json_str = to_json(config)
        deserialized = from_json(ButtonConfig, json_str)

        assert deserialized.entity_type == EntityType.BUTTON
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.event == config.event
        assert deserialized.event_data == {}
        assert deserialized.device_class is None

    def test_button_config_with_event_data(self):
        config = ButtonConfig(
            servent_id="test_servent",
            name="Test Button",
            event="button_pressed",
            event_data={"button_id": 1, "action": "press"},
        )

        json_str = to_json(config)
        deserialized = from_json(ButtonConfig, json_str)

        assert deserialized.event == config.event
        assert deserialized.event_data == config.event_data

    def test_button_config_with_device_class(self):
        config = ButtonConfig(
            servent_id="test_servent",
            name="Restart Button",
            event="restart_event",
            device_class="restart",
        )

        json_str = to_json(config)
        deserialized = from_json(ButtonConfig, json_str)

        assert deserialized.device_class == "restart"

    def test_button_config_full(self):
        config = ButtonConfig(
            servent_id="test_servent",
            name="Test Button",
            event="button_event",
            event_data={"key": "value", "number": 42},
            device_class="update",
            entity_category="config",
            disabled_by_default=False,
        )

        json_str = to_json(config)
        deserialized = from_json(ButtonConfig, json_str)

        assert deserialized.entity_type == EntityType.BUTTON
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.event == config.event
        assert deserialized.event_data == config.event_data
        assert deserialized.device_class == config.device_class
        assert deserialized.entity_category == config.entity_category
        assert deserialized.disabled_by_default == config.disabled_by_default
