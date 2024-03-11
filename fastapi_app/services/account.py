from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi_app import crud, models
from .base import BaseService


class AccountsService(BaseService):
    db: AsyncSession

    def __init__(self, db: AsyncSession, user_id: UUID):
        self.db = db
        self.user_id = user_id

    async def create_account(self) -> models.Account:
        return await crud.Account(db=self.db).create(models.AccountCreate())
