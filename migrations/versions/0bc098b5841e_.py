"""empty message

Revision ID: 0bc098b5841e
Revises: 
Create Date: 2023-06-06 13:09:21.876812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0bc098b5841e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('diameter', sa.String(length=30), nullable=True),
    sa.Column('rotation_period', sa.Integer(), nullable=True),
    sa.Column('orbital_period', sa.Integer(), nullable=True),
    sa.Column('gravity', sa.String(length=30), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=30), nullable=True),
    sa.Column('terrain', sa.String(length=30), nullable=True),
    sa.Column('surface_water', sa.Integer(), nullable=True),
    sa.Column('created', sa.String(length=30), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_name', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=50), nullable=True),
    sa.Column('mail', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mail'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('favorite_planet',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('peoples',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('height', sa.Float(), nullable=True),
    sa.Column('mass', sa.Float(), nullable=True),
    sa.Column('hair_color', sa.String(length=30), nullable=True),
    sa.Column('skin_color', sa.String(length=30), nullable=True),
    sa.Column('eye_color', sa.String(length=30), nullable=True),
    sa.Column('birth_year', sa.String(length=30), nullable=True),
    sa.Column('gender', sa.String(length=30), nullable=True),
    sa.Column('created', sa.String(length=30), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('homeworld', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['homeworld'], ['planets.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('url')
    )
    op.create_table('favorite_people',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id'], ['peoples.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite_people')
    op.drop_table('peoples')
    op.drop_table('favorite_planet')
    op.drop_table('users')
    op.drop_table('planets')
    # ### end Alembic commands ###