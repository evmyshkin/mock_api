"""Инициализация схемы processor_schema с таблицами requests/settings/modes.

Revision ID: b7c8d9e0f1a2
Revises: a1b2c3d4e5f6
Create Date: 2026-04-18 16:30:00.000000

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op
from sqlalchemy.dialects import postgresql

# Идентификаторы ревизии, используемые Alembic.
revision: str = 'b7c8d9e0f1a2'
down_revision: str | Sequence[str] | None = 'a1b2c3d4e5f6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    schema_upgrades()
    data_upgrades()


def downgrade() -> None:
    data_downgrades()
    schema_downgrades()


def schema_upgrades() -> None:
    """Создать schema/table структуру processor."""
    op.execute('CREATE SCHEMA IF NOT EXISTS processor_schema')

    op.create_table(
        'post_modes',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('error_message', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        schema='processor_schema',
    )

    op.create_table(
        'status_modes',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        schema='processor_schema',
    )

    op.create_table(
        'status_mode_steps',
        sa.Column('status_mode_id', sa.Integer(), nullable=False),
        sa.Column('step_order', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('error_message', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['status_mode_id'], ['processor_schema.status_modes.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('status_mode_id', 'step_order', name='uq_processor_step_order'),
        sa.UniqueConstraint('status_mode_id', 'status', name='uq_processor_step_status'),
        schema='processor_schema',
    )

    op.create_table(
        'settings',
        sa.Column('endpoint_type', sa.String(), nullable=False),
        sa.Column('response_delay', sa.Integer(), nullable=False),
        sa.Column('response_code', sa.Integer(), nullable=False),
        sa.Column('status_mode_id', sa.Integer(), nullable=False),
        sa.Column('post_mode_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['post_mode_id'], ['processor_schema.post_modes.id']),
        sa.ForeignKeyConstraint(['status_mode_id'], ['processor_schema.status_modes.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('endpoint_type'),
        schema='processor_schema',
    )

    op.create_table(
        'requests',
        sa.Column('endpoint_type', sa.String(), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('request_id', sa.String(), nullable=False),
        sa.Column('order_id', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=False),
        sa.Column('post_mode_id', sa.Integer(), nullable=False),
        sa.Column('response_delay', sa.Integer(), nullable=False),
        sa.Column('response_code', sa.Integer(), nullable=False),
        sa.Column('status_mode_id', sa.Integer(), nullable=False),
        sa.Column('status_step_id', sa.Integer(), nullable=False),
        sa.Column('status_change_after', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('unixtimestamp', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['post_mode_id'], ['processor_schema.post_modes.id']),
        sa.ForeignKeyConstraint(['status_mode_id'], ['processor_schema.status_modes.id']),
        sa.ForeignKeyConstraint(['status_step_id'], ['processor_schema.status_mode_steps.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('request_id'),
        schema='processor_schema',
    )


def schema_downgrades() -> None:
    """Удалить schema/table структуру processor."""
    op.drop_table('requests', schema='processor_schema')
    op.drop_table('settings', schema='processor_schema')
    op.drop_table('status_mode_steps', schema='processor_schema')
    op.drop_table('status_modes', schema='processor_schema')
    op.drop_table('post_modes', schema='processor_schema')
    op.execute('DROP SCHEMA IF EXISTS processor_schema CASCADE')


def data_upgrades() -> None:
    """Сидирование базовых настроек processor-режимов и endpoint settings."""
    post_modes_table = sa.table(
        'post_modes',
        sa.column('id', sa.Integer()),
        sa.column('name', sa.String()),
        sa.column('error_message', postgresql.JSONB()),
        schema='processor_schema',
    )
    op.bulk_insert(
        post_modes_table,
        [
            {'id': 1, 'name': 'POST_DEFAULT', 'error_message': None},
            {
                'id': 2,
                'name': 'POST_ERROR',
                'error_message': {
                    'validationError': {
                        'detail': [
                            {
                                'loc': ['body', 'order_id'],
                                'msg': 'Эмулированная ошибка валидации отправки',
                                'type': 'value_error.processor.mock_error_response',
                            }
                        ]
                    }
                },
            },
        ],
    )

    status_modes_table = sa.table(
        'status_modes',
        sa.column('id', sa.Integer()),
        sa.column('name', sa.String()),
        schema='processor_schema',
    )
    op.bulk_insert(
        status_modes_table,
        [
            {'id': 1, 'name': 'FULFILLMENT_SUCCESS'},
            {'id': 2, 'name': 'FULFILLMENT_FAILED'},
        ],
    )

    status_steps_table = sa.table(
        'status_mode_steps',
        sa.column('id', sa.Integer()),
        sa.column('status_mode_id', sa.Integer()),
        sa.column('step_order', sa.Integer()),
        sa.column('status', sa.String()),
        sa.column('duration', sa.Integer()),
        sa.column('error_message', postgresql.JSONB()),
        schema='processor_schema',
    )
    op.bulk_insert(
        status_steps_table,
        [
            {
                'id': 1,
                'status_mode_id': 1,
                'step_order': 1,
                'status': 'Заказ получен',
                'duration': 5,
                'error_message': None,
            },
            {
                'id': 2,
                'status_mode_id': 1,
                'step_order': 2,
                'status': 'Оплата подтверждена',
                'duration': 5,
                'error_message': None,
            },
            {
                'id': 3,
                'status_mode_id': 1,
                'step_order': 3,
                'status': 'Упаковка',
                'duration': 5,
                'error_message': None,
            },
            {
                'id': 4,
                'status_mode_id': 1,
                'step_order': 4,
                'status': 'Отправлен',
                'duration': 5,
                'error_message': None,
            },
            {
                'id': 5,
                'status_mode_id': 1,
                'step_order': 5,
                'status': 'Доставлен',
                'duration': 5,
                'error_message': None,
            },
            {
                'id': 6,
                'status_mode_id': 2,
                'step_order': 1,
                'status': 'Заказ получен',
                'duration': 5,
                'error_message': None,
            },
            {
                'id': 7,
                'status_mode_id': 2,
                'step_order': 2,
                'status': 'Ошибка оплаты',
                'duration': 5,
                'error_message': [
                    {
                        'Paths': ['payment_method'],
                        'ProcessorCode': 'OP_16',
                        'ErrorCode': 'INVALID_VALUE',
                        'Annotation': 'Эмулированная ошибка валидации оплаты',
                    }
                ],
            },
        ],
    )

    settings_table = sa.table(
        'settings',
        sa.column('id', sa.Integer()),
        sa.column('endpoint_type', sa.String()),
        sa.column('response_delay', sa.Integer()),
        sa.column('response_code', sa.Integer()),
        sa.column('status_mode_id', sa.Integer()),
        sa.column('post_mode_id', sa.Integer()),
        schema='processor_schema',
    )
    op.bulk_insert(
        settings_table,
        [
            {
                'id': 1,
                'endpoint_type': 'submit',
                'response_delay': 0,
                'response_code': 200,
                'status_mode_id': 1,
                'post_mode_id': 1,
            },
            {
                'id': 2,
                'endpoint_type': 'status',
                'response_delay': 0,
                'response_code': 200,
                'status_mode_id': 1,
                'post_mode_id': 1,
            },
        ],
    )


def data_downgrades() -> None:
    """Опциональный откат сид-данных."""
    op.execute('DELETE FROM processor_schema.settings')
    op.execute('DELETE FROM processor_schema.status_mode_steps')
    op.execute('DELETE FROM processor_schema.status_modes')
    op.execute('DELETE FROM processor_schema.post_modes')
