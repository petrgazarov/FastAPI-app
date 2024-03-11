from typing import TYPE_CHECKING, Union, Callable, ClassVar, Any, Dict
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlmodel import Relationship, Field, ForeignKey
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from .base import SQLModelBase, PydanticModelBase

if TYPE_CHECKING:
    from .account import Account
    from .event_documentation import EventDocumentation


class EventSchema(SQLModelBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "event_schemas"

    json_schema: Dict[str, Any] = Field(default={}, sa_column=Column(JSONB))
    account_id: UUID = Field(
        sa_column=Column(
            SA_UUID(as_uuid=True),
            ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
    )
    event_documentation_id: UUID = Field(
        sa_column=Column(
            SA_UUID(as_uuid=True),
            ForeignKey("event_documentations.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
    )

    event_documentation: "EventDocumentation" = Relationship(
        back_populates="event_schema"
    )
    account: "Account" = Relationship(back_populates="event_schemas")


class EventSchemaCreate(PydanticModelBase):
    json_schema: Dict[str, Any]
    account_id: UUID
    event_documentation_id: UUID


class EventSchemaUpdate(PydanticModelBase):
    json_schema: Dict[str, Any]
