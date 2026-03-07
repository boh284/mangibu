from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# sqlite:/// → tipo di database
# ./ricettario.db → file nella cartella corrente
engine = create_engine(
    "sqlite:///./ricettario.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()