from contextlib import contextmanager

from django.conf import settings

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations.

    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    """
    Session = settings.SNOWFLAKE['session']
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()