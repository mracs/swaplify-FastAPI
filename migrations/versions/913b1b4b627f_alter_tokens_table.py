"""alter tokens table

Revision ID: 913b1b4b627f
Revises: 9207e0e47c5d
Create Date: 2021-10-15 15:55:11.793072

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '913b1b4b627f'
down_revision = '9207e0e47c5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('token', postgresql.UUID(), nullable=False))
    op.add_column('tokens', sa.Column('source', sa.Text(), nullable=True))
    op.drop_column('tokens', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_column('tokens', 'source')
    op.drop_column('tokens', 'token')
    # ### end Alembic commands ###
