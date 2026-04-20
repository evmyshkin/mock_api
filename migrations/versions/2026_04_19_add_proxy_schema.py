"""Добавление схемы proxy_schema с таблицами requests/settings.

Revision ID: c9d0e1f2a3b4
Revises: b7c8d9e0f1a2
Create Date: 2026-04-19 10:00:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects import postgresql

# Идентификаторы ревизии, используемые Alembic.
revision: str = 'c9d0e1f2a3b4'
down_revision: str | Sequence[str] | None = 'b7c8d9e0f1a2'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    schema_upgrades()
    data_upgrades()


def downgrade() -> None:
    data_downgrades()
    schema_downgrades()


def schema_upgrades() -> None:
    """Создать schema/table структуру proxy."""
    op.execute('CREATE SCHEMA IF NOT EXISTS proxy_schema')

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
        schema='proxy_schema',
    )

    op.create_table(
        'requests',
        sa.Column('request_id', sa.String(), nullable=False),
        sa.Column('query_params', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('headers', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('body', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_id'),
        schema='proxy_schema',
    )


def schema_downgrades() -> None:
    """Удалить schema/table структуру proxy."""
    op.drop_table('requests', schema='proxy_schema')
    op.drop_table('settings', schema='proxy_schema')
    op.execute('DROP SCHEMA IF EXISTS proxy_schema CASCADE')


def data_upgrades() -> None:
    """Сидирование настроек proxy capture endpoint."""
    settings_table = sa.table(
        'settings',
        sa.column('endpoint_type', sa.String()),
        sa.column('response_delay', sa.Integer()),
        sa.column('response_code', sa.Integer()),
        schema='proxy_schema',
    )

    op.bulk_insert(
        settings_table,
        [
            {
                'endpoint_type': 'capture',
                'response_delay': 0,
                'response_code': 200,
            }
        ],
    )


def data_downgrades() -> None:
    """Опциональный откат сид-данных."""
    op.execute('DELETE FROM proxy_schema.settings')
