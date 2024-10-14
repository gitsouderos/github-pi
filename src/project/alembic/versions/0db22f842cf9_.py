"""vectors

Revision ID: 0db22f842cf9
Revises: 9ab5262fd5f1
Create Date: 2024-10-02 10:31:40.299995

"""

from typing import Sequence, Union

from alembic import op
import pgvector
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0db22f842cf9"
down_revision: Union[str, None] = "9ab5262fd5f1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "embeddings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "embedding", pgvector.sqlalchemy.vector.VECTOR(dim=1024), nullable=False
        ),
        sa.Column("file_id", sa.Integer(), nullable=False),
        sa.Column("inserted_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["file_id"],
            ["content_files.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("embeddings")
    op.execute("DROP EXTENSTION IF EXISTS vector")
    # ### end Alembic commands ###
