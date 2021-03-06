"""empty message

Revision ID: 5286455174e5
Revises: d88b169c4958
Create Date: 2017-09-18 13:22:39.647000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5286455174e5'
down_revision = 'd88b169c4958'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('employeesadmin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employeesadmin',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('username', mysql.VARCHAR(length=60), nullable=True),
    sa.Column('password_hash', mysql.VARCHAR(length=128), nullable=True),
    sa.Column('is_admin', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset=u'utf8',
    mysql_engine=u'InnoDB'
    )
    # ### end Alembic commands ###
