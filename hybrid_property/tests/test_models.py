from app.models import Stats

def test_filter_by_age_seconds(db_session):
    stats = Stats()
    db_session.add(stats)
    db_session.flush()

    assert db_session.query(Stats).filter(Stats.age_seconds > 100).first() is not None