from serde.json import from_json, to_json

from servents.data_model.entity_configs import DeviceConfig


class TestDeviceConfig:
    def test_device_config_minimal(self):
        config = DeviceConfig(
            device_id="test_device",
            name="Test Device",
        )

        json_str = to_json(config)
        assert json_str is not None

        deserialized = from_json(DeviceConfig, json_str)
        assert deserialized.device_id == config.device_id
        assert deserialized.name == config.name
        assert deserialized.manufacturer is None
        assert deserialized.model is None
        assert deserialized.version is None
        assert deserialized.app_name is None
        assert deserialized.is_global is False

    def test_device_config_full(self):
        config = DeviceConfig(
            device_id="test_device",
            name="Test Device",
            manufacturer="Test Manufacturer",
            model="Test Model",
            version="1.0.0",
            app_name="test_app",
            is_global=True,
        )

        json_str = to_json(config)
        deserialized = from_json(DeviceConfig, json_str)

        assert deserialized.device_id == config.device_id
        assert deserialized.name == config.name
        assert deserialized.manufacturer == config.manufacturer
        assert deserialized.model == config.model
        assert deserialized.version == config.version
        assert deserialized.app_name == config.app_name
        assert deserialized.is_global == config.is_global
