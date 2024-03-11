from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from .base import CRUDBase
from fastapi_app import models


class EmailAlreadyExistsError(Exception):
    pass


class User(CRUDBase[models.User, models.UserCreate, models.UserUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = models.User

    async def create(self, data: models.UserCreate) -> models.User:
        try:
            return await super().create(data)
        except IntegrityError as e:
            if "UniqueViolationError" in str(object=e) and "email" in str(object=e):
                raise EmailAlreadyExistsError(
                    f"User with this email already exists. Try signing in with your original SSO provider."
                ) from e
            raise e
