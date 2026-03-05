from fastapi import FastAPI, HTTPException, status, APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List, Literal

router = APIRouter(prefix="/ricette", tags=["Ricette"])

app=FastAPI(title="prima app", description="api di esempio")

class Ingredienti(BaseModel):
    nome:str
    quantita:str
    opzionale:bool=False

class Ricetta(BaseModel):
    nome:str=Field(
        ...,
        min_length=2,
        max_length=100
    )
    ingredienti: List[Ingredienti]
    porzioni: int=Field(
        default=4, 
        ge=1,
        le=20
    )
    tempoPreparazione: int=Field(
        gt=0
    )
    difficolta: Literal["facile", "media", "difficile"]="media"
    
ricetteDb:dict= {}
prossimoId:int =1
    
@router.post("/",status_code=201)
def postRicetta(ricetta:Ricetta):
    global prossimoId
    ricetteDb[prossimoId]={"id":prossimoId, **ricetta.model_dump()}
    prossimoId+=1
    return getRicetta(prossimoId-1)


@router.get("/{idRicetta}")
def getRicetta(idRicetta:int):
    if not idRicetta in ricetteDb:
        raise HTTPException(status_code=404, detail="Ricetta non trovata")
    return ricetteDb[idRicetta]
    
@router.put("/{idRicetta}")
def putRicetta(idRicetta:int, ricetta:Ricetta):
    if not idRicetta in ricetteDb:
        raise HTTPException(status_code=404, detail="Ricetta non trovata")
    ricetteDb[idRicetta]={"id":idRicetta, **ricetta.model_dump()}
    return ricetteDb[idRicetta]

@router.delete("/{idRicetta}", status_code=204)
def removeRicetta(idRicetta:int):
    if not idRicetta in ricetteDb:
        raise HTTPException(status_code=404, detail="Ricetta non trovata")
    del ricetteDb[idRicetta]
    
@router.get("/")
def filtri(difficolta: Optional[str]=None,maxMinuti:Optional[int]=None,porzioni:Optional[int]=None):
    print("ciap")
    risultati=list(ricetteDb.values())
    if difficolta is not None:
        risultati=[r for r in risultati if difficolta==r.get("difficolta")]
    if maxMinuti is not None:
        risultati=[r for r in risultati if r.get("tempoPreparazione")<=maxMinuti]
    if porzioni is not None:
        risultati=[r for r in risultati if r.get("porzioni")>=porzioni]
    return risultati