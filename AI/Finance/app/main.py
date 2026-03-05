from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
import crud
import uvicorn
import os


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="Finance App",
    description=" Backend for analytics and trading research.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to the Financial Portfolio API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/assets")
def add_asset(symbol: str, name: str, asset_class: str, db: Session = Depends(get_db)):
    return crud.create_asset(db, symbol, name, asset_class)

@app.get("/assets")
def list_assets(db: Session = Depends(get_db)):
    return crud.get_assets(db)


# if __name__ == "__main__":
#     os.chdir(r"C:\Users\nickc\Desktop\Code\Personal Projects\AI\Finance\app")
#     os.system(r'C:/Users/nickc/AppData/Local/Programs/Python/Python311/python.exe -m uvicorn main:app --reload')
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)