"""create_devices_table

Revision ID: 40659bc66128
Revises: 
Create Date: 2025-05-18 05:14:37.231587

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '40659bc66128'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create devices table."""
    op.create_table(
        'devices',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=False),
        sa.Column('system_name', sa.String(), nullable=True),  # новое поле
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('ip_address')
    )


def downgrade() -> None:
    """Drop devices table."""
    op.drop_table('devices')
