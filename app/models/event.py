from typing import TYPE_CHECKING, Dict, List, Union, Callable, ClassVar, Any, Optional
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from datetime import datetime
from sqlmodel import Relationship, Field, ForeignKey
from sqlalchemy import Column, Index, text
from sqlalchemy.dialects.postgresql import JSONB
from .base import SQLModelBase, PydanticModelBase

if TYPE_CHECKING:
    from .account import Account
    from .screenshot import Screenshot
    from .event_documentation_example import EventDocumentationExample


class Event(SQLModelBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "events"

    __table_args__ = (
        Index("index_events_on_name_and_account_id", "name", "account_id"),
    )

    name: str = Field()
    path: str = Field()
    domain: str = Field()
    provider: str = Field()
    properties: Dict[str, Any] = Field(sa_column=Column(JSONB))
    account_id: UUID = Field(
        sa_column=Column(
            SA_UUID(as_uuid=True),
            ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": text("current_timestamp(0)")},
        index=True,
    )

    account: "Account" = Relationship(back_populates="events")
    screenshot: "Screenshot" = Relationship(
        back_populates="event", sa_relationship_kwargs={"uselist": False}
    )
    event_documentation_example: Optional["EventDocumentationExample"] = Relationship(
        back_populates="event", sa_relationship_kwargs={"uselist": False}
    )


class EventCreate(PydanticModelBase):
    name: str
    path: str
    domain: str
    provider: str
    properties: Dict[str, Any]
    account_id: UUID
