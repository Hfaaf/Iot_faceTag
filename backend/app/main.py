from fastapi import FastAPI
from app.database import init_db

app = FastAPI(title="FaceTag API")


@app.lifespan("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"status": "ok", "message": "FaceTag backend funcionando"}
