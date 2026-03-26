"""add is_active to pets

Revision ID: c3f7a12d9e01
Revises: ad5ff1f2280b
Create Date: 2026-03-25 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3f7a12d9e01'
down_revision: Union[str, None] = 'ad5ff1f2280b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'pets',
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true'))
    )


def downgrade() -> None:
    op.drop_column('pets', 'is_active')
