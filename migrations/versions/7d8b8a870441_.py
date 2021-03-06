"""empty message

Revision ID: 7d8b8a870441
Revises: 
Create Date: 2020-09-17 21:46:57.094099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d8b8a870441'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('phone_number', sa.Text(), nullable=False),
    sa.Column('profession', sa.Text(), nullable=True),
    sa.Column('business_type', sa.Text(), nullable=True),
    sa.Column('location', sa.Text(), nullable=True),
    sa.Column('orders', sa.Integer(), nullable=True),
    sa.Column('gender', sa.Text(), nullable=True),
    sa.Column('age', sa.Text(), nullable=True),
    sa.Column('price_category', sa.Text(), nullable=True),
    sa.Column('action', sa.Text(), nullable=True),
    sa.Column('action_price', sa.Float(), nullable=True),
    sa.Column('budget', sa.Float(), nullable=True),
    sa.Column('site', sa.Text(), nullable=True),
    sa.Column('site_url', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('phone_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
