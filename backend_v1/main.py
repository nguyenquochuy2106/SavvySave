from fastapi import FastAPI
from backend.services.auth import auth_router
from backend.services.transactions import transactions_router
from backend.services.stats import stats_router
from backend.services.users import users_router

app = FastAPI(title="SavvySave API")

# Registering routes
app.include_router(auth_router, prefix="/auth")
app.include_router(transactions_router, prefix="/transactions")
app.include_router(stats_router, prefix="/stats")
app.include_router(users_router, prefix="/users")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
