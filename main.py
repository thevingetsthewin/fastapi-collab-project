from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TranslationTip(BaseModel):
    id: int
    english: str
    mandarin: str
    category: str

database = []

@app.post("/add_tip/")
def add_tip(tip: TranslationTip):
    database.append(tip)
    return {"message": "Tip added successfully!", "data": tip}