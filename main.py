from fastapi import FastAPI

app=FastAPI(title="prima app", description="api di esempio")

@app.get("/")
def getRoot():
    return {"messaggio":"Ciao"}
