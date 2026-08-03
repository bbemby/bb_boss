"""add privacy_mode to emby

Revision ID: 20260803_01
Revises: 20260315_02
Create Date: 2026-08-03 08:30:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260803_01"
down_revision = "20260315_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    column_names = {column["name"] for column in inspector.get_columns("emby")}
    if "privacy_mode" not in column_names:
        op.add_column("emby", sa.Column("privacy_mode", sa.Boolean(), nullable=True, server_default=sa.text("0")))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    column_names = {column["name"] for column in inspector.get_columns("emby")}
    if "privacy_mode" in column_names:
        op.drop_column("emby", "privacy_mode")
