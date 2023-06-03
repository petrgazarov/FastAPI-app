from uuid import UUID
from app import models


class ScreenshotCreate(models.PydanticModelBase):
    image_data: bytes
    content_type: str
    account_id: UUID
    event_id: UUID
