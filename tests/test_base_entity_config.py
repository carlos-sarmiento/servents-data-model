from serde.json import from_json, to_json

from servents.data_model.entity_configs import DeviceConfig, EntityConfig
from servents.data_model.entity_types import EntityType


class TestEntityConfig:
    def test_entity_config_minimal(self):
        config = EntityConfig(
            entity_type=EntityType.SENSOR,
            servent_id="test_servent",
            name="Test Entity",
        )

        json_str = to_json(config)
        deserialized = from_json(EntityConfig, json_str)

        assert deserialized.entity_type == config.entity_type
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.default_state is None
        assert deserialized.fixed_attributes == {}
        assert deserialized.entity_category is None
        assert deserialized.disabled_by_default is False
        assert deserialized.app_name is None
        assert deserialized.device_definition is None

    def test_entity_config_with_device(self):
        device = DeviceConfig(
            device_id="test_device",
            name="Test Device",
        )

        config = EntityConfig(
            entity_type=EntityType.SENSOR,
            servent_id="test_servent",
            name="Test Entity",
            device_definition=device,
        )

        json_str = to_json(config)
        deserialized = from_json(EntityConfig, json_str)

        assert deserialized.device_definition is not None
        assert deserialized.device_definition.device_id == device.device_id
        assert deserialized.device_definition.name == device.name

    def test_entity_config_full(self):
        config = EntityConfig(
            entity_type=EntityType.SENSOR,
            servent_id="test_servent",
            name="Test Entity",
            default_state=42.5,
            fixed_attributes={"key1": "value1", "key2": 123},
            entity_category="diagnostic",
            disabled_by_default=True,
            app_name="test_app",
        )

        json_str = to_json(config)
        deserialized = from_json(EntityConfig, json_str)

        assert deserialized.entity_type == config.entity_type
        assert deserialized.servent_id == config.servent_id
        assert deserialized.name == config.name
        assert deserialized.default_state == config.default_state
        assert deserialized.fixed_attributes == config.fixed_attributes
        assert deserialized.entity_category == config.entity_category
        assert deserialized.disabled_by_default == config.disabled_by_default
        assert deserialized.app_name == config.app_name

    def test_entity_config_default_state_types(self):
        config_str = EntityConfig(
            entity_type=EntityType.SENSOR,
            servent_id="test",
            name="Test",
            default_state="test_value",
        )
        json_str = to_json(config_str)
        deserialized = from_json(EntityConfig, json_str)
        assert deserialized.default_state == "test_value"

        config_bool = EntityConfig(
            entity_type=EntityType.BINARY_SENSOR,
            servent_id="test",
            name="Test",
            default_state=True,
        )
        json_str = to_json(config_bool)
        deserialized = from_json(EntityConfig, json_str)
        assert deserialized.default_state is True

        config_int = EntityConfig(
            entity_type=EntityType.NUMBER,
            servent_id="test",
            name="Test",
            default_state=42,
        )
        json_str = to_json(config_int)
        deserialized = from_json(EntityConfig, json_str)
        assert deserialized.default_state == 42

        config_float = EntityConfig(
            entity_type=EntityType.NUMBER,
            servent_id="test",
            name="Test",
            default_state=3.14,
        )
        json_str = to_json(config_float)
        deserialized = from_json(EntityConfig, json_str)
        assert deserialized.default_state == 3.14
