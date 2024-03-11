from typing import TYPE_CHECKING, Union, Callable, ClassVar
from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlmodel import Relationship, Field, Column, ForeignKey
from .base import SQLModelBase, PydanticModelBase

if TYPE_CHECKING:
    from .account import Account


class Domain(SQLModelBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "domains"

    name: str = Field()
    account_id: UUID = Field(
        sa_column=Column(
            SA_UUID(as_uuid=True),
            ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
    )

    account: "Account" = Relationship(back_populates="domains")


class DomainCreate(PydanticModelBase):
    name: str
    account_id: UUID
