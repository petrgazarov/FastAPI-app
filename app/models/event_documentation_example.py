from typing import TYPE_CHECKING, Union, Callable, ClassVar
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlmodel import Relationship, Field, Column, ForeignKey
from .base import SQLModelBase, PydanticModelBase

if TYPE_CHECKING:
    from .account import Account
    from .event import Event
    from .event_documentation import EventDocumentation


class EventDocumentationExample(SQLModelBase, table=True):
    __tablename__: ClassVar[
        Union[str, Callable[..., str]]
    ] = "event_documentation_examples"

    event_documentation_id: UUID = Field(
        sa_column=Column(
            SA_UUID(as_uuid=True),
            ForeignKey("event_documentations.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
    )
    event_id: UUID = Field(
        sa_column=Column(
            SA_UUID(as_uuid=True),
            ForeignKey("events.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
            unique=True,
        ),
    )
    account_id: UUID = Field(
        sa_column=Column(
            SA_UUID(as_uuid=True),
            ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
    )

    event_documentation: "EventDocumentation" = Relationship(
        back_populates="event_documentation_examples",
    )
    event: "Event" = Relationship(back_populates="event_documentation_example")
    account: "Account" = Relationship()


class EventDocumentationExampleCreate(PydanticModelBase):
    event_documentation_id: UUID
    event_id: UUID
    account_id: UUID
