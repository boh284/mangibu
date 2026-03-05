from fastapi import FastAPI
from routers import ricette, piani

app = FastAPI(title="Ricettario")
app.include_router(ricette.router)
app.include_router(piani.router)
