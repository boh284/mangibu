from pydantic import BaseModel, Field
from typing import Optional, List, Literal

class Ingredienti(BaseModel):
    nome: str
    quantita: str
    opzionale: bool = False

class Ricetta(BaseModel):
    nome: str = Field(..., min_length=2, max_length=40)
    ingredienti: List[Ingredienti]
    porzioni: int = Field(default=4, ge=1, le=20)
    tempoPreparazione: int = Field(..., gt=0)
    difficolta: Literal["facile", "media", "difficile"] = "media"
    
class Piano(BaseModel):
    giorno: str
    nome: str = Field(..., min_length=2, max_length=40)
    tipoPasto: Literal["colazione", "spuntino", "pranzo", "merenda", "cena"] = "colazione"
    ricetta: Ricetta