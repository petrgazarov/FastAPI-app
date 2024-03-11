from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as SA_UUID
from sqlmodel import Field, Column, ForeignKey
from fastapi_app.utils.s3_client import s3_client
from .base import SQLModelBase, PydanticModelBase


class BaseFile(SQLModelBase):
    file_key: str = Field(index=True)
    content_type: str = Field()
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
        raise NotImplementedError("Subclasses must implement this property")

    def image_url(self) -> str:
        signed_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name(), "Key": self.file_key},
            ExpiresIn=3600,  # URL valid for 1 hour (3600 seconds)
        )
        return signed_url


class BaseFileCreate(PydanticModelBase):
    file_key: str
    content_type: str
    account_id: UUID
