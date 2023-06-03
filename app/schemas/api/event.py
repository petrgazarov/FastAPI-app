from typing import Any, Dict
from uuid import UUID
from app import models


class EventCreate_EventData(models.PydanticModelBase):
    name: str
    path: str
    domain: str
    provider: str
    properties: Dict[str, Any]
    image_data: str


class EventCreate(models.PydanticModelBase):
    event_data: EventCreate_EventData
    write_key: UUID
