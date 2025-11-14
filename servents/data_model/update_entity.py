from dataclasses import dataclass, field
from typing import Any

from serde import serde


@serde
@dataclass
class ServentUpdateEntity:
    servent_id: str
    state: Any | None
    attributes: dict = field(default_factory=dict)
