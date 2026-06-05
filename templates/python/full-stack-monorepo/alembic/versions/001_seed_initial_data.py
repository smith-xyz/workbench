"""Seed initial data

Revision ID: 001_seed_data
Revises: 
Create Date: 2024-01-01 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Boolean, Integer

# revision identifiers, used by Alembic.
revision: str = '001_seed_data'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Define the table structure for data insertion
    users_table = table('users',
        column('id', Integer),
        column('email', String),
        column('name', String),
        column('is_active', Boolean)
    )
    
    # Insert seed data
    op.bulk_insert(users_table, [
        {'email': 'admin@example.com', 'name': 'Admin User', 'is_active': True},
        {'email': 'user@example.com', 'name': 'Regular User', 'is_active': True},
        {'email': 'inactive@example.com', 'name': 'Inactive User', 'is_active': False},
    ])


def downgrade() -> None:
    # Remove seed data
    op.execute("DELETE FROM users WHERE email IN ('admin@example.com', 'user@example.com', 'inactive@example.com')")
