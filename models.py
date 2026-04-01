from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class RicettaDB(Base):
    __tablename__ = "ricette"   # nome della tabella nel file .db

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    porzioni = Column(Integer, default=4)
    tempoPreparazione = Column(Integer, nullable=False)
    difficolta = Column(String, default="media")
    ingredienti = relationship("RicettaIngredienteDB", lazy="joined")
    proprietarioId = Column(Integer, ForeignKey("utenti.id"), nullable=False)
    proprietario = relationship("UtenteDB", lazy="joined")
    condivisioni = relationship("CondivisioniDB", lazy="joined")

    
class PianoDB(Base):
    __tablename__ = "piani"
    
    id = Column(Integer, primary_key=True, index=True)
    giorno = Column(String, nullable=False)
    nome = Column(String, nullable=False)
    tipoPasto = Column(String, nullable=False)
    ricettaId = Column(Integer, ForeignKey("ricette.id"), nullable=True)
    ricetta = relationship("RicettaDB", lazy="joined")
    proprietarioId = Column(Integer, ForeignKey("utenti.id"), nullable=False)
    proprietario = relationship("UtenteDB", lazy="joined")
    
class IngredienteDB(Base):
    __tablename__ = "ingredienti"
    
    id=Column(Integer, primary_key=True, index=False)
    nome=Column(String, nullable=False)
    
class RicettaIngredienteDB(Base):
    __tablename__ = "ricetta_ingredienti"
    
    ricettaId=Column(Integer, ForeignKey("ricette.id"), nullable=False, primary_key=True)
    ingredienteId=Column(Integer, ForeignKey("ingredienti.id"), nullable=False, primary_key=True)
    quantita=Column(String, nullable=False)
    facoltativo=Column(Boolean, nullable=False)
    ingrediente=relationship("IngredienteDB", lazy="joined")

class UtenteDB(Base):
    __tablename__="utenti"
    
    id=Column(Integer, primary_key=True, index=True)
    username=Column(String, nullable=False, unique=True)
    email=Column(String, nullable=False, unique=True)
    passwordHash=Column(String, nullable=False)
    attivo=Column(Boolean, default=True)

class CondivisioniDB(Base):
    __tablename__="ricette_condivise"
    
    ricettaId=Column(Integer, ForeignKey("ricette.id"), nullable=False, primary_key=True)
    utenteId=Column(Integer, ForeignKey("utenti.id"), nullable=False, primary_key=True)
    utente = relationship("UtenteDB", lazy="joined")
