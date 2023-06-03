"""create users table

Revision ID: b4a56b178155
Revises: e8fe31da6e29
Create Date: 2023-04-05 15:51:21.095825

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = "b4a56b178155"
down_revision = "e8fe31da6e29"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4),
        sa.Column("email", sa.String, nullable=False, unique=True, index=True),
        # first_name and last_name are optional because name is optional in GitHub API
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("image_url", sa.String),
        sa.Column("supertokens_id", sa.String, nullable=False, unique=True, index=True),
        sa.Column(
            "account_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accounts.id"),
            nullable=True,
            index=True,
        ),
        sa.Column(
            "created_at", sa.DateTime, server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("users")
