from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class RicettaDB(Base):
    __tablename__ = "ricette"   # nome della tabella nel file .db

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    porzioni = Column(Integer, default=4)
    tempoPreparazione = Column(Integer, nullable=False)
    difficolta = Column(String, default="media")
    
class PianoDB(Base):
    __tablename__ = "piani"
    
    id = Column(Integer, primary_key=True, index=True)
    giorno = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    tipoPasto = Column(String, nullable=False)
    ricettaId = Column(Integer, ForeignKey("ricette.id"), nullable=True)
    ricetta = relationship("RicettaDB", lazy="joined")