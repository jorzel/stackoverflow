import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import create_engine, MetaData, func, text, Interval, literal, UniqueConstraint, Index
from sqlalchemy.orm import declarative_base, configure_mappers
from sqlalchemy.sql.functions import coalesce

from datetime import datetime, timedelta

DB_URI = "postgresql://postgres:postgres@localhost:5432/testdb"
engine = create_engine(DB_URI)
metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Stats(Base):
    __tablename__ = "stats"

    id = sa.Column(sa.Integer, primary_key=True)
    data = sa.Column(MutableDict.as_mutable(psql.JSONB))
    max_age_ms = sa.Column(sa.Integer(), index=False, nullable=False, server_default='10000')
    x = sa.Column(sa.Integer, nullable=True)
    created = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        Index('x_uc', func.coalesce(x, 1000), unique=True),
    )


    @hybrid_property
    def age_seconds(self):
        utc_now = datetime.utcnow()
        return (utc_now - self.created).seconds

    @age_seconds.expression
    def age_seconds(cls):
        return func.date_part('second', func.timezone('UTC', func.now()) - cls.created)

    @hybrid_property
    def purge_dt(self):
        utc_now = datetime.utcnow()
        return utc_now - timedelta(seconds=self.max_age_ms/1000)

    @purge_dt.expression
    def purge_dt(cls):
        seconds_delta = literal('1 second').cast(Interval) * (cls.max_age_ms / 1000)
        return func.timezone('UTC', func.now()) - seconds_delta
    
configure_mappers()