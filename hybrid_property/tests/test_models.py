from app.models import Stats

def test_filter_by_age_seconds(db_session):
    stats = Stats()
    db_session.add(stats)
    db_session.flush()

    assert db_session.query(Stats).filter(Stats.age_seconds > 100).first() is None

def test_filter_by_purge_dt(db_session):
    stats = Stats()
    stats2 = Stats(x=1)
    db_session.add(stats)
    db_session.add(stats2)
    db_session.flush()

    assert db_session.query(Stats).filter(Stats.purge_dt < '2022-07-06 12:10:55').first() is None