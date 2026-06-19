from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from app.config import DATABASE_PATH

Base = declarative_base()

_engine = None
_SessionFactory = None


def init_db():
    global _engine, _SessionFactory
    _engine = create_engine(
        f"sqlite:///{DATABASE_PATH}",
        connect_args={"check_same_thread": False},
        echo=False,
    )
    _SessionFactory = sessionmaker(bind=_engine, expire_on_commit=False)
    from app.database.models import Base  # noqa
    Base.metadata.create_all(_engine)


def get_session():
    if _SessionFactory is None:
        init_db()
    return scoped_session(_SessionFactory)


def dispose_engine():
    global _engine
    if _engine:
        _engine.dispose()
