from typing import Sequence, Optional, cast
from uuid import UUID
import base64
from app import crud, models
from app.schemas import api as schemas_api
from .base import BaseService


class EventsService(BaseService):
    async def create_event(
        self, event_data: schemas_api.EventCreate_EventData
    ) -> models.Event:
        event = await crud.Event(db=self.db).create(
            models.EventCreate(
                name=event_data.name,
                path=event_data.path,
                domain=event_data.domain,
                provider=event_data.provider,
                properties=event_data.properties,
                account_id=self.account_id,
            )
        )
        if event:
            decoded_image_data = base64.b64decode(event_data.image_data.split(",")[1])
            await crud.Screenshot(db=self.db).create(
                schemas_api.ScreenshotCreate(
                    image_data=decoded_image_data,
                    content_type="image/jpeg",
                    account_id=self.account_id,
                    event_id=event.id,
                )
            )
        return event

    async def delete_events_by_name(self, name: str) -> bool:
        return await crud.Event(db=self.db).delete_by_name(
            name=name, account_id=self.account_id
        )

    async def delete_all_events(self) -> bool:
        await crud.Event(db=self.db).delete_all({"account_id": self.account_id})
        await crud.EventDocumentation(db=self.db).delete_all(
            {"account_id": self.account_id}
        )
        return True
