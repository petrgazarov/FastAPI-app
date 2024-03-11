from uuid import uuid4
from io import BytesIO
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from fastapi_app import models
from fastapi_app.utils.s3_client import s3_client
from fastapi_app.schemas import api as schemas_api
from .base import CRUDBase


class Screenshot(
    CRUDBase[
        models.Screenshot,
        schemas_api.ScreenshotCreate,
        BaseModel,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = models.Screenshot

    async def create(self, data: schemas_api.ScreenshotCreate) -> models.Screenshot:
        file_key = f"{data.account_id}/{str(uuid4())}.jpeg"
        s3_client.upload_fileobj(
            BytesIO(data.image_data),
            self.model.bucket_name(),
            file_key,
            ExtraArgs={"ContentType": data.content_type},
        )

        db_instance = models.Screenshot.from_orm(
            models.ScreenshotCreate(
                file_key=file_key,
                content_type=data.content_type,
                account_id=data.account_id,
                event_id=data.event_id,
            )
        )
        self.db.add(db_instance)
        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e
        await self.db.refresh(db_instance)
        return db_instance
