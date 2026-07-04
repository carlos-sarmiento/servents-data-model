from serde import from_dict
from serde.json import from_json, to_json

from servents.data_model.update_entity import ServentUpdateEntity


class TestServentUpdateEntity:
    def test_update_entity_state_is_optional(self):
        update = from_dict(
            ServentUpdateEntity,
            {"servent_id": "test_servent", "available": False},
        )

        assert update.servent_id == "test_servent"
        assert update.state is None
        assert update.attributes == {}
        assert update.available is False
        assert update.merge_attributes is None

    def test_update_entity_full_payload_roundtrip(self):
        update = ServentUpdateEntity(
            servent_id="test_servent",
            state={"state": True, "brightness": 128},
            attributes={"source": "test"},
            available=True,
            merge_attributes=True,
        )

        json_str = to_json(update)
        deserialized = from_json(ServentUpdateEntity, json_str)

        assert deserialized.servent_id == update.servent_id
        assert deserialized.state == update.state
        assert deserialized.attributes == update.attributes
        assert deserialized.available is True
        assert deserialized.merge_attributes is True
