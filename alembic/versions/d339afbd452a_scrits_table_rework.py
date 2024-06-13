"""scrits table rework

Revision ID: d339afbd452a
Revises: 49a8927d3cc3
Create Date: 2024-05-29 21:54:28.469863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd339afbd452a'
down_revision: Union[str, None] = '49a8927d3cc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scripts', sa.Column('inspection_status', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('scripts', 'inspection_status')
    # ### end Alembic commands ###