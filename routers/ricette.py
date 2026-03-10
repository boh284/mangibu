from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from schemas import Ricetta
from database import get_db
from models import RicettaDB, IngredienteDB, RicettaIngredienteDB

router = APIRouter(prefix="/ricette", tags=["Ricette"])

@router.post("/", status_code=201)
def postRicetta(ricetta: Ricetta, db: Session = Depends(get_db)):
    nuova = RicettaDB(
        nome=ricetta.nome,
        porzioni=ricetta.porzioni,
        tempoPreparazione=ricetta.tempoPreparazione,
        difficolta=ricetta.difficolta
    )
    db.add(nuova)       
    db.flush()
    
    for ing in ricetta.ingredienti:
        ingrediente = db.query(IngredienteDB).filter(IngredienteDB.nome==ing.nome).first()
        if not ingrediente:
            ingrediente = IngredienteDB(
                nome=ing.nome
            )
            db.add(ingrediente)
            db.flush()
            
        nuovoLegame=RicettaIngredienteDB(
            ricettaId=nuova.id,
            ingredienteId=ingrediente.id,
            quantita=ing.quantita,
            facoltativo=ing.facoltativo
        )
        
        db.add(nuovoLegame)
        
    db.commit()
    return nuova

@router.get("/")
def filtri(difficolta: Optional[str] = None, maxMinuti: Optional[int] = None, porzioni: Optional[int] = None, db: Session = Depends(get_db)):
    
    risultati = db.query(RicettaDB).all()
    
    if difficolta is not None:
        risultati = [r for r in risultati if difficolta == r.difficolta]
    if maxMinuti is not None:
        risultati = [r for r in risultati if r.tempoPreparazione <= maxMinuti]
    if porzioni is not None:
        risultati = [r for r in risultati if r.porzioni >= porzioni]
    return risultati

@router.get("/{idRicetta}")
def getRicetta(idRicetta: int, db: Session = Depends(get_db)):
    ricetta = db.query(RicettaDB).filter(RicettaDB.id == idRicetta).first()
    if ricetta is None:
        raise HTTPException(status_code=404, detail="Ricetta non trovata")
    return ricetta

@router.put("/{idRicetta}")
def putRicetta(idRicetta: int, ricetta: Ricetta, db: Session = Depends(get_db)):
    esistente = db.query(RicettaDB).filter(RicettaDB.id == idRicetta).first()
    if esistente is None:
        raise HTTPException(status_code=404, detail="Ricetta non trovata")
    esistente.nome = ricetta.nome
    esistente.porzioni = ricetta.porzioni
    esistente.tempoPreparazione = ricetta.tempoPreparazione
    esistente.difficolta = ricetta.difficolta
    
    db.commit()
    db.refresh(esistente)
    return esistente

@router.delete("/{idRicetta}", status_code=204)
def removeRicetta(idRicetta: int, db: Session = Depends(get_db)):
    ricetta=db.query(RicettaDB).filter(RicettaDB.id == idRicetta).first()
    if ricetta is None:
        raise HTTPException(status_code=404, detail="Ricetta non trovata")
    db.delete(ricetta)
    db.commit()