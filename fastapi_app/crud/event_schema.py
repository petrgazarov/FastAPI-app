from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_app import models
from pydantic import BaseModel
from .base import CRUDBase


class EventSchema(CRUDBase[models.EventSchema, models.EventSchemaCreate, BaseModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = models.EventSchema
