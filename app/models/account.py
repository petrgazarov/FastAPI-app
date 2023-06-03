from typing import List, TYPE_CHECKING, Union, Callable, ClassVar
from sqlalchemy import text
from uuid import uuid4, UUID
from sqlmodel import Field, Relationship
from .base import SQLModelBase, PydanticModelBase

if TYPE_CHECKING:
    from .event import Event
    from .event_schema import EventSchema
    from .event_documentation import EventDocumentation
    from .screenshot import Screenshot
    from .domain import Domain
    from .user import User


class Account(SQLModelBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "accounts"

    write_key: UUID = Field(
        default_factory=uuid4,
        index=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()"), "unique": True},
    )

    events: List["Event"] = Relationship(back_populates="account")
    event_schemas: List["EventSchema"] = Relationship(back_populates="account")
    event_documentations: List["EventDocumentation"] = Relationship(
        back_populates="account"
    )
    screenshots: List["Screenshot"] = Relationship(back_populates="account")
    domains: List["Domain"] = Relationship(back_populates="account")
    users: List["User"] = Relationship(back_populates="account")


class AccountCreate(PydanticModelBase):
    pass
