import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from app.core.config import database

metadata = sqlalchemy.MetaData()

tokens_table = sqlalchemy.Table(
    'tokens',
    metadata,
    sqlalchemy.Column(
        'token',
        UUID(),
        primary_key=True,
        unique=True
    ),
    sqlalchemy.Column('source', sqlalchemy.Text),
    sqlalchemy.Column('user_ip', sqlalchemy.String(15)),
    sqlalchemy.Column('expires', sqlalchemy.DateTime()),
)


async def get_source_by_token(token):
    query = (
        sqlalchemy.select(
            [tokens_table.c.source]
        )
        .select_from(tokens_table)
        .where(tokens_table.c.token == token)
    )
    return await database.fetch_val(query)
