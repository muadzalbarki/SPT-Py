from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from app.paths import get_data_root

DATABASE_PATH = get_data_root() / "data" / "spt_dprd.db"

Base = declarative_base()

_engine = None
_SessionFactory = None


def init_db():
    global _engine, _SessionFactory
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _engine = create_engine(
        f"sqlite:///{DATABASE_PATH.as_posix()}",
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
