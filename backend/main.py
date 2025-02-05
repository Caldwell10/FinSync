from fastapi import FastAPI
from backend.app.routes.transactions import router as transactions_router
from backend.app.routes import auth, budget
app = FastAPI()

app.include_router(auth.router)
app.include_router(transactions_router)
app.include_router(budget.router)

@app.get("/")
def home():
    return {"message" : "FinSync API is running"}

