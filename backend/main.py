from fastapi import FastAPI
from backend.routes import auth, transactions, budget

app = FastAPI(title="SavvySave API", version="1.0")

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
app.include_router(budget.router, prefix="/budget", tags=["Budget"])

@app.get("/")
def root():
    return {"message": "Welcome to SavvySave API!"}
