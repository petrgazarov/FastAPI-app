from sqlalchemy import delete
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession
from app import models
from pydantic import BaseModel
from .base import CRUDBase


class Event(CRUDBase[models.Event, models.EventCreate, BaseModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = models.Event

    async def delete_by_name(self, name: str, account_id: UUID4) -> bool:
        stmt = (
            delete(self.model)
            .where(self.model.name == name)
            .where(self.model.account_id == account_id)
        )
        await self.db.execute(stmt)
        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e
        return True
