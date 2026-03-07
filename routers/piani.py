from fastapi import APIRouter, HTTPException
from typing import Optional
from schemas import Piano

router = APIRouter(prefix="/piani", tags=["Piani"])

pianiDb: dict = {}
prossimoId: int = 1

@router.get("/")
def getPiani():
    return list(pianiDb.values())

@router.get("/{idPiano}")
def getPiano(idPiano: int):
    if idPiano not in pianiDb:
        raise HTTPException(status_code=404, detail="Piano non trovato")
    return pianiDb[idPiano]

@router.post("/", status_code=201)
def postPiano(piano: Piano):
    global prossimoId
    pianiDb[prossimoId] = {"id": prossimoId, **piano.model_dump()}
    prossimoId += 1
    return getPiano(prossimoId - 1)