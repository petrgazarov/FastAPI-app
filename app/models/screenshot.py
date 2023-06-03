from typing import TYPE_CHECKING, Union, Callable, ClassVar
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlmodel import Relationship, Field, Column, ForeignKey
from .base_file import BaseFile, BaseFileCreate

if TYPE_CHECKING:
    from .account import Account
    from .event import Event


class Screenshot(BaseFile, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "screenshots"

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

    @classmethod
    def bucket_name(cls) -> str:
        return "glaza-screenshots"

    event: "Event" = Relationship(back_populates="screenshot")
    account: "Account" = Relationship(back_populates="screenshots")


class ScreenshotCreate(BaseFileCreate):
    event_id: UUID
