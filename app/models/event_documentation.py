from typing import TYPE_CHECKING, List, Union, Callable, ClassVar
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from datetime import datetime
from sqlmodel import Relationship, Field, ARRAY, String, Column, ForeignKey
from sqlalchemy import Index
from .base import SQLModelBase, PydanticModelBase

if TYPE_CHECKING:
    from .account import Account
    from .event_documentation_example import EventDocumentationExample
    from .event_schema import EventSchema


class EventDocumentation(SQLModelBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "event_documentations"

    name: str = Field()
    last_seen: datetime = Field()
    domains: List[str] = Field(
        sa_column=Column(ARRAY(String), default=lambda: [], nullable=False)
    )
    paths: List[str] = Field(
        sa_column=Column(ARRAY(String), default=lambda: [], nullable=False)
    )
    account_id: UUID = Field(
        sa_column=Column(
            SA_UUID(as_uuid=True),
            ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
    )

    event_documentation_examples: List["EventDocumentationExample"] = Relationship(
        back_populates="event_documentation",
    )
    event_schema: "EventSchema" = Relationship(
        back_populates="event_documentation", sa_relationship_kwargs={"uselist": False}
    )
    account: "Account" = Relationship(back_populates="event_documentations")

    __table_args__ = (
        Index(
            "index_event_documentations_on_name_and_account_id", "name", "account_id"
        ),
    )


class EventDocumentationCreate(PydanticModelBase):
    name: str
    last_seen: datetime
    account_id: UUID
    domains: List[str]
    paths: List[str]


class EventDocumentationUpdate(PydanticModelBase):
    last_seen: datetime
