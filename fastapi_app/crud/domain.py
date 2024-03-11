from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from .base import CRUDBase
from fastapi_app import models


class Domain(CRUDBase[models.Domain, models.DomainCreate, BaseModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = models.Domain
