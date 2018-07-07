"""empty message

Revision ID: dd25651d5f6b
Revises: 8f3c231cfccf
Create Date: 2018-07-07 12:02:19.677039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd25651d5f6b'
down_revision = '8f3c231cfccf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('album', sa.Column('purchased', sa.Boolean(), server_default=sa.text('0'), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('album', 'purchased')
    # ### end Alembic commands ###
