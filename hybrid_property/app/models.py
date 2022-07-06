import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import create_engine, MetaData, func
from sqlalchemy.orm import declarative_base, configure_mappers

from datetime import datetime

DB_URI = "postgresql://postgres:postgres@localhost:5432/testdb"
engine = create_engine(DB_URI)
metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Stats(Base):
    __tablename__ = "stats"

    id = sa.Column(sa.Integer, primary_key=True)
    data = sa.Column(MutableDict.as_mutable(psql.JSONB))
    max_age_ms = sa.Column(sa.Integer(), index=False, nullable=False, server_default='1000')
    created = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)

    @hybrid_property
    def age_seconds(self):
        utc_now = datetime.utcnow()
        return (utc_now - self.created).seconds

    @age_seconds.expression
    def age_seconds(cls):
        return func.date_part('second', func.timezone('UTC', func.now()) - cls.created)


configure_mappers()