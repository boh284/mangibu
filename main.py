from fastapi import FastAPI
from routers import ricette

app = FastAPI(title="Ricettario")
app.include_router(ricette.router)