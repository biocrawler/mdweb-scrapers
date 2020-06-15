"""empty message

Revision ID: 8ea1a28d873d
Revises: 41417aed1ff0
Create Date: 2020-06-14 20:11:24.543462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ea1a28d873d'
down_revision = '41417aed1ff0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('article', sa.Column('digital_object_id', sa.String(length=128), nullable=True))
    op.add_column('article', sa.Column('title', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('article', 'title')
    op.drop_column('article', 'digital_object_id')
    op.drop_table('file')
    # ### end Alembic commands ###
