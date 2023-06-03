from typing import Any, Dict, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import ColumnElement, select
from sqlalchemy.orm import joinedload, selectinload
from pydantic import BaseModel
from app import models
from .base import CRUDBase


class EventDocumentation(
    CRUDBase[models.EventDocumentation, models.EventDocumentationCreate, BaseModel]
):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.model = models.EventDocumentation

    async def find_all_with_schemas(
        self, where: Dict[str, Any] = {}, order_by: Optional[ColumnElement] = None
    ) -> Sequence[models.EventDocumentation]:
        filters = [getattr(self.model, key) == value for key, value in where.items()]
        stmt = (
            select(self.model)
            .where(*filters)
            .options(joinedload("event_schema"))
            .options(
                selectinload("event_documentation_examples")
                .selectinload("event")
                .selectinload("screenshot")
            )
        )

        if order_by is not None:
            stmt = stmt.order_by(order_by)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def find_by_with_schema(
        self, where: Dict[str, Any]
    ) -> Optional[models.EventDocumentation]:
        filters = [getattr(self.model, key) == value for key, value in where.items()]
        stmt = (
            select(self.model)
            .where(*filters)
            .options(joinedload(self.model.event_schema))
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()
