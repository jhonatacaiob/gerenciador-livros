"""Adiciona data de publicação no model do livro

Revision ID: 22c706bd729d
Revises: 66d71de93456
Create Date: 2024-06-08 01:03:41.322112
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '22c706bd729d'
down_revision: Union[str, None] = '66d71de93456'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'livro', sa.Column('data_publicacao', sa.Date(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('livro', 'data_publicacao')
    # ### end Alembic commands ###
