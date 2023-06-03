from typing import Dict, Any, List
from datetime import datetime
from uuid import UUID
from app import models


class EventDocumentationsGet_EventSchema(models.PydanticModelBase):
    json_schema: Dict[str, Any]


class EventDocumentationsGet_Screenshot(models.PydanticModelBase):
    id: UUID
    image_url: str


class EventDocumentationsGet_Event(models.PydanticModelBase):
    id: UUID
    name: str
    path: str
    domain: str
    provider: str
    properties: Dict[str, Any]
    screenshot: EventDocumentationsGet_Screenshot


class EventDocumentationsGet_EventDocumentationExample(models.PydanticModelBase):
    id: UUID
    event: EventDocumentationsGet_Event


class EventDocumentationsGet(models.PydanticModelBase):
    id: UUID
    name: str
    last_seen: datetime
    domains: List[str]
    paths: List[str]
    event_schema: EventDocumentationsGet_EventSchema
    event_documentation_examples: List[EventDocumentationsGet_EventDocumentationExample]
