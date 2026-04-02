"""merge heads fix

Revision ID: merge_heads_fix
Revises: c1a2b3d4e5f6, c3f7a12d9e01
Create Date: 2026-04-02

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'merge_heads_fix'
down_revision: Union[str, Sequence[str], None] = ('c1a2b3d4e5f6', 'c3f7a12d9e01')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
