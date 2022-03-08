"""table chat created

Revision ID: 197b8374dedd
Revises: 8df9865d27e9
Create Date: 2022-03-08 20:44:27.695012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '197b8374dedd'
down_revision = '8df9865d27e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chats',
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.PrimaryKeyConstraint('chat_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('chats')
    # ### end Alembic commands ###
