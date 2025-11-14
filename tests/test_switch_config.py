from serde.json import from_json, to_json

from servents.data_model.entity_configs import (
    SwitchConfig,
)
from servents.data_model.entity_types import EntityType


class TestSwitchConfig:
    def test_switch_config_minimal(self):
        config = SwitchConfig(
            servent_id="test_servent",
            name="Test Switch",
        )

        json_str = to_json(config)
        deserialized = from_json(SwitchConfig, json_str)

        assert deserialized.entity_type == EntityType.SWITCH
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.device_class is None

    def test_switch_config_with_device_class(self):
        config = SwitchConfig(
            servent_id="test_servent",
            name="Power Outlet",
            device_class="outlet",
        )

        json_str = to_json(config)
        deserialized = from_json(SwitchConfig, json_str)

        assert deserialized.device_class == "outlet"

    def test_switch_config_full(self):
        config = SwitchConfig(
            servent_id="test_servent",
            name="Test Switch",
            device_class="switch",
            default_state=False,
            entity_category="config",
            disabled_by_default=True,
        )

        json_str = to_json(config)
        deserialized = from_json(SwitchConfig, json_str)

        assert deserialized.entity_type == EntityType.SWITCH
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.device_class == config.device_class
        assert deserialized.default_state == config.default_state
        assert deserialized.entity_category == config.entity_category
        assert deserialized.disabled_by_default == config.disabled_by_default
