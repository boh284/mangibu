from fastapi import FastAPI
from routers import ricette, piani
from database import engine, Base
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ricettario")
app.include_router(ricette.router)
app.include_router(piani.router)
