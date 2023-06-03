from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app import models
from .base import CRUDBase


class EventDocumentationExample(
    CRUDBase[
        models.EventDocumentationExample,
        models.EventDocumentationExampleCreate,
        BaseModel,
    ]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = models.EventDocumentationExample
