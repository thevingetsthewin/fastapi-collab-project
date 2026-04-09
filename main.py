from fastapi import FastAPI
from pydantic import BaseModel
import json

class Term(BaseModel):
    id: int
    english: str
    mandarin: str
    category: str

app = FastAPI()

def load_database() -> list:
    try:
        with open("translations.json","r",encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

@app.get("/")
def read_root():
    return {"message": "Welcome to the translation API. Use /terms to view all translations, /terms/id/{id} to see a specific translation by its ID and /terms/category/{category} to see translations by category."}

@app.get("/terms", response_model=list[Term])
def get_terms():
    """Returns a list of all terms in the database."""
    data = load_database()
    return data
@app.get("/terms/id/{term_id}", response_model=Term)
def get_term_by_id(term_id: int):
    """Returns a specific term using its ID."""
    data = load_database() 
    if term_id < 1 or term_id > len(data):
        return {"error": "Term not found"}
    return data[term_id - 1]
@app.get("/terms/category/{category}", response_model=list[Term])
def get_term_by_category(category: str):
    """Returns all terms that belong to a specified category."""
    data = load_database()
    results = [term for term in data if term.get("category") == category]
    return results

@app.post("/terms/add")
def add_term(newTerm: Term):
    """Adds a new term to the database."""
    data = load_database()
    data.append(newTerm.model_dump())

    with open("translations.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return {"message": "Successfully added new term.", "term": newTerm}