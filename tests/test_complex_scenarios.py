from serde.json import from_json, to_json

from servents.data_model.entity_configs import (
    DeviceConfig,
    NumberConfig,
    SensorConfig,
    SwitchConfig,
)


class TestComplexScenarios:
    def test_entity_with_complex_device(self):
        device = DeviceConfig(
            device_id="complex_device",
            name="Complex Device",
            manufacturer="Test Manufacturer",
            model="Model X",
            version="2.0.0",
            app_name="test_app",
            is_global=True,
        )

        config = SensorConfig(
            servent_id="test_servent",
            name="Device Sensor",
            device_class="temperature",
            unit_of_measurement="°C",
            device_definition=device,
        )

        json_str = to_json(config)
        deserialized = from_json(SensorConfig, json_str)

        assert deserialized.device_definition is not None
        assert deserialized.device_definition.device_id == device.device_id
        assert deserialized.device_definition.manufacturer == device.manufacturer
        assert deserialized.device_definition.model == device.model
        assert deserialized.device_definition.version == device.version
        assert deserialized.device_definition.app_name == device.app_name
        assert deserialized.device_definition.is_global == device.is_global

    def test_multiple_configs_roundtrip(self):
        configs = [
            SensorConfig(
                servent_id="sensor1",
                name="Sensor 1",
                device_class="temperature",
            ),
            NumberConfig(
                servent_id="number1",
                name="Number 1",
                mode="slider",
            ),
            SwitchConfig(
                servent_id="switch1",
                name="Switch 1",
            ),
        ]

        for config in configs:
            json_str = to_json(config)
            assert json_str is not None

            deserialized = None
            if isinstance(config, SensorConfig):
                deserialized = from_json(SensorConfig, json_str)
            elif isinstance(config, NumberConfig):
                deserialized = from_json(NumberConfig, json_str)
            elif isinstance(config, SwitchConfig):
                deserialized = from_json(SwitchConfig, json_str)

            assert deserialized is not None
            assert deserialized.servent_id == config.servent_id
            assert deserialized.name == config.name
