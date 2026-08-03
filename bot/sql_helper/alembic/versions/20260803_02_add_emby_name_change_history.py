"""add emby_name_change_history table

Revision ID: 20260803_02
Revises: 20260803_01
Create Date: 2026-08-03 23:00:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260803_02"
down_revision = "20260803_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'emby_name_change_history',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tg', sa.BigInteger(), nullable=False, comment='TG用户ID'),
        sa.Column('tg_username', sa.String(255), nullable=True, comment='TG用户名/昵称'),
        sa.Column('embyid', sa.String(255), nullable=True, comment='Emby用户ID'),
        sa.Column('old_name', sa.String(255), nullable=True, comment='修改前用户名'),
        sa.Column('new_name', sa.String(255), nullable=False, comment='修改后用户名'),
        sa.Column('cost', sa.Integer(), nullable=True, default=0, comment='消耗积分'),
        sa.Column('created_at', sa.DateTime(), nullable=True, default=sa.func.now(), comment='修改时间'),
        sa.PrimaryKeyConstraint('id'),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
    )


def downgrade() -> None:
    op.drop_table('emby_name_change_history')
