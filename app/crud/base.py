from typing import Generic, Sequence, Optional, TypeVar, Type, Dict, Any
from sqlmodel import select, delete
from pydantic import UUID4
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import ColumnElement
from app import models

ModelType = TypeVar("ModelType", bound=models.SQLModelBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    db: AsyncSession
    model: Type[ModelType]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def find(self, id: UUID4) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by(self, kwargs: Dict[str, Any]) -> Optional[ModelType]:
        filters = [getattr(self.model, key) == value for key, value in kwargs.items()]
        stmt = select(self.model).where(*filters)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all(
        self, where: Dict[str, Any] = {}, order_by: Optional[ColumnElement] = None
    ) -> Sequence[ModelType]:
        filters = [getattr(self.model, key) == value for key, value in where.items()]
        stmt = select(self.model).where(*filters)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, data: CreateSchemaType) -> ModelType:
        instance = self.model.from_orm(data)
        self.db.add(instance)
        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e
        await self.db.refresh(instance)
        return instance

    async def update(
        self,
        instance: ModelType,
        data: UpdateSchemaType,
    ) -> ModelType:
        data = data.dict(exclude_unset=True)
        for key, value in data.items():
            setattr(instance, key, value)
        self.db.add(instance)
        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e
        await self.db.refresh(instance)
        return instance

    async def delete(self, id: UUID4) -> ModelType:
        instance = await self.find(id)
        if instance is None:
            raise Exception(f"{self.model.__name__} not found")
        try:
            await self.db.delete(instance)
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e
        return instance

    async def delete_all(self, where: Dict[str, Any]) -> bool:
        filters = [getattr(self.model, key) == value for key, value in where.items()]
        stmt = delete(self.model).where(*filters)
        await self.db.execute(stmt)
        try:
            await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e
        return True
