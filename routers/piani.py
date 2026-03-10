from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from schemas import Piano
from sqlalchemy.orm import Session
from database import get_db
from models import PianoDB, RicettaDB

router = APIRouter(prefix="/piani", tags=["Piani"])

@router.get("/")
def getPiani(db : Session= Depends(get_db)):
    return db.query(PianoDB).all()

@router.get("/{idPiano}")
def getPiano(idPiano: int, db: Session=Depends(get_db)):
    piano = db.query(PianoDB).filter(PianoDB.id == idPiano).first()
    if piano is None:
        raise HTTPException(status_code=404, detail="Piano non trovato")
    return piano

@router.post("/", status_code=201)
def postPiano(piano: Piano, db: Session=Depends(get_db)):
    if piano.ricettaId is not None:
        ricetta = db.query(RicettaDB).filter(RicettaDB.id == piano.ricettaId).first()
        if ricetta is None:
            raise HTTPException(status_code=404, detail="Ricetta non trovata")
        
    nuovo = PianoDB(
        giorno=piano.giorno,
        nome=piano.nome,
        tipoPasto=piano.tipoPasto,
        ricettaId=piano.ricettaId
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo