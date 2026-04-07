from fastapi import FastAPI
import json

app = FastAPI()

def load_database():
    with open("translations.json","r",encoding="utf-8") as f:
        return json.load(f)
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the translation API. Use /terms to view all translations, /terms/id/{id} to see a specific translation by its ID and /terms/category/{category} to see translations by category."}

@app.get("/terms")
def get_terms():
    """Returns a list of all terms in the database."""
    data = load_database()
    return data
@app.get("/terms/id/{term_id}")
def get_term_by_id(term_id: int):
    """Returns a specific term using its ID."""
    data = load_database()
    if term_id < 1 or term_id > len(data):
        return {"error": "Term not found"}
    return data[term_id - 1]
@app.get("/terms/category/{category}")
def get_term_by_category(category: str):
    """Returns all terms that belong to a specified category."""
    data = load_database()
    results = [term for term in data if term.get("category") == category]
    return results