from app.models import metadata, DB_URI, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

import pytest


@pytest.fixture(scope="session")
def db_connection():
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    connection = engine.connect()

    yield connection

    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def db_session(db_connection):
    transaction = db_connection.begin()
    session = sessionmaker(bind=db_connection)
    session = session()

    yield session

    transaction.rollback()
    session.close()
