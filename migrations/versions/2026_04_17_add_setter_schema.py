"""Инициализация схемы setter_schema с таблицами requests/settings.

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-04-17 15:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects import postgresql

# Идентификаторы ревизии, используемые Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    schema_upgrades()
    data_upgrades()


def downgrade() -> None:
    data_downgrades()
    schema_downgrades()


def schema_upgrades() -> None:
    """Создать schema/table структуру setter."""
    op.execute('CREATE SCHEMA IF NOT EXISTS setter_schema')

    op.create_table(
        'requests',
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('is_validated', sa.Boolean(), server_default=sa.text('False'), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='setter_schema',
    )

    op.create_table(
        'settings',
        sa.Column('endpoint_type', sa.String(), nullable=False),
        sa.Column('response_delay', sa.Integer(), nullable=False),
        sa.Column('response_code', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('endpoint_type'),
        schema='setter_schema',
    )


def schema_downgrades() -> None:
    """Удалить schema/table структуру setter."""
    op.drop_table('settings', schema='setter_schema')
    op.drop_table('requests', schema='setter_schema')
    op.execute('DROP SCHEMA IF EXISTS setter_schema CASCADE')


def data_upgrades() -> None:
    """Сидирование настроек setter эндпоинтов."""
    settings_table = sa.table(
        'settings',
        sa.column('endpoint_type', sa.String()),
        sa.column('response_delay', sa.Integer()),
        sa.column('response_code', sa.Integer()),
        schema='setter_schema',
    )
    op.bulk_insert(
        settings_table,
        [
            {'endpoint_type': 'get_products', 'response_delay': 0, 'response_code': 200},
        ],
    )


def data_downgrades() -> None:
    """Опциональный откат сид-данных."""
    op.execute('DELETE FROM setter_schema.settings')
