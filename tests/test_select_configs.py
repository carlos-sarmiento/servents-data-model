from serde.json import from_json, to_json

from servents.data_model.entity_configs import (
    SelectConfig,
)
from servents.data_model.entity_types import EntityType


class TestSelectConfig:
    def test_select_config_minimal(self):
        config = SelectConfig(
            servent_id="test_servent",
            name="Test Select",
            options=["option1", "option2", "option3"],
        )

        json_str = to_json(config)
        deserialized = from_json(SelectConfig, json_str)

        assert deserialized.entity_type == EntityType.SELECT
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert list(deserialized.options) == ["option1", "option2", "option3"]

    def test_select_config_full(self):
        config = SelectConfig(
            servent_id="test_servent",
            name="Test Select",
            options=["low", "medium", "high"],
            default_state="medium",
            entity_category="config",
            disabled_by_default=False,
        )

        json_str = to_json(config)
        deserialized = from_json(SelectConfig, json_str)

        assert deserialized.entity_type == EntityType.SELECT
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert list(deserialized.options) == list(config.options)
        assert deserialized.default_state == config.default_state
        assert deserialized.entity_category == config.entity_category
        assert deserialized.disabled_by_default == config.disabled_by_default
