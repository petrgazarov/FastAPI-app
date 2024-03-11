from typing import Optional, List
from uuid import UUID
from fastapi_app import models


class UserGet_Domain(models.PydanticModelBase):
    id: UUID
    name: str


class UserGet_Account(models.PydanticModelBase):
    id: UUID
    write_key: UUID
    domains: List[UserGet_Domain]


class UserGet(models.PydanticModelBase):
    id: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    email: str
    image_url: Optional[str]
    account: Optional[UserGet_Account]


class UserUpdate(models.PydanticModelBase):
    first_name: Optional[str]
    last_name: Optional[str]
