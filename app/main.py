from fastapi import FastAPI
from app.routers import user, expense , balance_sheet  # Import your routers

app = FastAPI()

# Include your routers
app.include_router(user.router)
app.include_router(expense.router)
app.include_router(balance_sheet.router)


@app.get("/")
def read_root():
    return {"message": "Expense Management API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
