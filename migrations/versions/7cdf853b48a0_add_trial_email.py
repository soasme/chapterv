"""add trial email

Revision ID: 7cdf853b48a0
Revises: 4aefcdb88349
Create Date: 2016-02-02 09:22:13.689352

"""

# revision identifiers, used by Alembic.
revision = '7cdf853b48a0'
down_revision = '4aefcdb88349'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trial_email',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email', name='uk_trial_email_email')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trial_email')
    ### end Alembic commands ###
