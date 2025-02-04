from fastapi import FastAPI
from sqlalchemy.sql.functions import user

from backend.app.config.database import engine, Base
from backend.app.routes import auth

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
def home():
    return {"message" : "FinSync API is running"}

