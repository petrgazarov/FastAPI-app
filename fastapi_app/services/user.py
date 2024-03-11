from sqlmodel import select
from sqlalchemy.orm import joinedload
from fastapi_app import models, crud
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional


class UsersService:
    db: AsyncSession

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_with_account(self, supertokens_id: str) -> Optional[models.User]:
        stmt = (
            select(models.User)
            .where(models.User.supertokens_id == supertokens_id)
            .options(
                joinedload(models.User.account, innerjoin=False).selectinload(
                    models.Account.domains
                )
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, payload: models.UserCreate) -> Optional[models.User]:
        return await crud.User(db=self.db).create(payload)

    async def update_user(
        self, instance: models.User, payload: models.UserUpdate
    ) -> models.User:
        return await crud.User(db=self.db).update(instance, payload)
