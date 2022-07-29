# pylint: disable=no-member,invalid-name,unused-import

"""Role

Revision ID: f8bfefd4b530
Revises: 402096afc5b9
Create Date: 2022-07-18 13:50:27.728822

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel
import fastapi_utils
import common.datatypes.domain


# revision identifiers, used by Alembic.
revision = "f8bfefd4b530"
down_revision = "402096afc5b9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    table = op.create_table(
        "role",
        sa.Column(
            "id",
            fastapi_utils.guid_type.GUID(),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_role_name"), "role", ["name"], unique=True)
    # ### end Alembic commands ###
    if table is not None:
        op.bulk_insert(
            table,
            [
                {"name": common.datatypes.domain.Role.READER.value},
                {"name": common.datatypes.domain.Role.REVIEWER.value},
                {"name": common.datatypes.domain.Role.ADMINISTRATOR.value},
            ],
        )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_role_name"), table_name="role")
    op.drop_table("role")
    # ### end Alembic commands ###
