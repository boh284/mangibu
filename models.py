from sqlalchemy import Column, Integer, String
from database import Base

class RicettaDB(Base):
    __tablename__ = "ricette"   # nome della tabella nel file .db

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    porzioni = Column(Integer, default=4)
    tempoPreparazione = Column(Integer, nullable=False)
    difficolta = Column(String, default="media")