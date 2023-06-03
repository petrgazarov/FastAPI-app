"""create event_documentations table

Revision ID: 801047f6478c
Revises: b4a56b178155
Create Date: 2023-04-29 16:30:03.783890

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4


# revision identifiers, used by Alembic.
revision = "801047f6478c"
down_revision = "b4a56b178155"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "event_documentations",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4,
        ),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("last_seen", sa.DateTime, nullable=False),
        sa.Column("domains", sa.ARRAY(sa.String()), nullable=False, default=list),
        sa.Column("paths", sa.ARRAY(sa.String()), nullable=False, default=list),
        sa.Column(
            "account_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
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
    op.create_index(
        "index_event_documentations_on_name_and_account_id",
        "event_documentations",
        ["name", "account_id"],
        unique=False,
    )
    op.create_table(
        "event_schemas",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            default=uuid4,
        ),
        sa.Column(
            # nullable=False does not work correctly with SQLModel
            "json_schema",
            postgresql.JSONB,
        ),
        sa.Column(
            "account_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("accounts.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "event_documentation_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("event_documentations.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
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
    op.drop_table("event_schemas")
    op.drop_table("event_documentations")
