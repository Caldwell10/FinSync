from fastapi import FastAPI
from app.config.database import engine, Base

app = FastAPI()

@app.get("/")
def home():
    return {"message" : "FinSync API is running"}

