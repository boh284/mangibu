from fastapi import FastAPI, HTTPException, status, APIRouter
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from ricette import Ricetta

router = APIRouter(prefix="/piani", tags=["Piani"])

class Piano(BaseModel):
    giorno:str
    nome:str=Field(
        ...,
        min_length=2,
        max_length=40
    )
    tipoPasto: Literal["colazione", "spuntino", "pranzo", "merenda", "cena"]="colazione"
    ricetta:Ricetta
    
pianiDb:dict={}
prossimoId:int=1

@router.get("/{idPiano}")
def getPiano(idPiano:int):
    if not idPiano in pianiDb:
        raise HTTPException(status_code=404, detail="Piano non trovato")
    return pianiDb[idPiano]

@router.post("/{idPiano}")
def postPiano(piano:Piano):
    global prossimoId
    pianiDb[prossimoId]={"id":prossimoId, **piano.model_dump()}
    prossimoId+=1
    return getPiano(prossimoId-1)


    