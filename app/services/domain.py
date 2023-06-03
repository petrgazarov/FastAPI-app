from typing import Optional
from app import crud, models
from .base import BaseService
from uuid import UUID


class DomainsService(BaseService):
    async def create_domain(self, domain: models.DomainCreate) -> models.Domain:
        return await crud.Domain(db=self.db).create(domain)

    async def delete_domain(self, id: UUID) -> models.Domain:
        return await crud.Domain(db=self.db).delete(id=id)
