from datetime import datetime
from sqlalchemy import text
from uuid import uuid4, UUID
from sqlmodel import Field, SQLModel
from pydantic import BaseModel


class SQLModelBase(SQLModel):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": text("gen_random_uuid()")},
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"server_default": text("current_timestamp(0)")},
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
            "onupdate": text("current_timestamp(0)"),
        },
    )


class PydanticModelBase(BaseModel):
    class Config:
        orm_mode = True
