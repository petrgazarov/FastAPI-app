from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_app import models
from pydantic import BaseModel
from .base import CRUDBase


class Account(CRUDBase[models.Account, models.AccountCreate, BaseModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = models.Account
