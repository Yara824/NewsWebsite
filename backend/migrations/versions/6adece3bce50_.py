"""empty message

Revision ID: 6adece3bce50
Revises: 
Create Date: 2023-04-18 11:31:17.867618

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6adece3bce50'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.String(length=500), nullable=False),
    sa.Column('timestamp_start', sa.DateTime(), nullable=True),
    sa.Column('experimental_condition', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_timestamp_start'), ['timestamp_start'], unique=False)

    op.create_table('exposures',
    sa.Column('user_id', sa.String(length=500), nullable=True),
    sa.Column('timestamp_exposures', sa.DateTime(), nullable=True),
    sa.Column('exposure_id', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('exposure_id')
    )
    with op.batch_alter_table('exposures', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_exposures_timestamp_exposures'), ['timestamp_exposures'], unique=False)

    op.create_table('positions',
    sa.Column('article_id', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.String(length=500), nullable=True),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('primary', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('primary')
    )
    op.create_table('reads',
    sa.Column('article_id', sa.String(length=50), nullable=True),
    sa.Column('read_title', sa.String(length=50), nullable=True),
    sa.Column('read_condition', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.String(length=500), nullable=True),
    sa.Column('timestamp_reads', sa.DateTime(), nullable=True),
    sa.Column('primary', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('primary')
    )
    with op.batch_alter_table('reads', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_reads_timestamp_reads'), ['timestamp_reads'], unique=False)

    op.create_table('selections',
    sa.Column('article_id', sa.String(length=50), nullable=True),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(length=500), nullable=True),
    sa.Column('timestamp_selections', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('condition', sa.String(length=50), nullable=True),
    sa.Column('primary', sa.String(length=500), nullable=False),
    sa.ForeignKeyConstraint(['position'], ['positions.position'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('primary')
    )
    with op.batch_alter_table('selections', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_selections_timestamp_selections'), ['timestamp_selections'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('selections', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_selections_timestamp_selections'))

    op.drop_table('selections')
    with op.batch_alter_table('reads', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_reads_timestamp_reads'))

    op.drop_table('reads')
    op.drop_table('positions')
    with op.batch_alter_table('exposures', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_exposures_timestamp_exposures'))

    op.drop_table('exposures')
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_timestamp_start'))

    op.drop_table('users')
    # ### end Alembic commands ###
