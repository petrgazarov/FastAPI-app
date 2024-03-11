from typing import TYPE_CHECKING, Optional, ClassVar, Union, Callable
from uuid import UUID
from sqlmodel import Relationship, Field
from .base import SQLModelBase, PydanticModelBase

if TYPE_CHECKING:
    from .account import Account


class User(SQLModelBase, table=True):
    __tablename__: ClassVar[Union[str, Callable[..., str]]] = "users"

    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    supertokens_id: str = Field(unique=True, index=True)
    account_id: Optional[UUID] = Field(
        default=None, foreign_key="accounts.id", index=True
    )

    account: Optional["Account"] = Relationship(back_populates="users")


class UserCreate(PydanticModelBase):
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    image_url: Optional[str]
    supertokens_id: str


class UserUpdate(PydanticModelBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    image_url: Optional[str] = None
    account_id: Optional[UUID] = None
