from fastapi import FastAPI, HTTPException, Query
from database import connect_to_mongodb
from bson import ObjectId
from typing import Optional

# -----------------------------------------------
# 1. Créer l'application
# -----------------------------------------------
app = FastAPI(title="Manga API", description="API pour gérer une collection de mangas", version="1.0")

# -----------------------------------------------
# 2. Connexion à MongoDB
# -----------------------------------------------
db = connect_to_mongodb()
if db is None:
    raise Exception("Connexion MongoDB échouée")

collection = db["mangas"]  # notre collection


# -----------------------------------------------
# HELPER : MongoDB renvoie des ObjectId,
# JSON ne sait pas les lire → on les convertit
# -----------------------------------------------
def format_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc


# -----------------------------------------------
# 3. SEED : insérer des données de base
#    (seulement si la collection est vide)
# -----------------------------------------------
@app.on_event("startup")
def seed():
    if collection.count_documents({}) == 0:
        collection.insert_many([
            {
                "titre": "Naruto",
                "description": "Un ninja qui veut devenir Hokage",
                "genre": "action",
                "note": 9
            },
            {
                "titre": "Death Note",
                "description": "Un lycéen trouve un carnet qui tue",
                "genre": "thriller",
                "note": 10
            },
            {
                "titre": "One Piece",
                "description": "Un pirate cherche le trésor ultime",
                "genre": "aventure",
                "note": 10
            }
        ])
        print("Données insérées")


# ===============================================
# LES ROUTES
# ===============================================

# -----------------------------------------------
# POST /items → Créer un manga
# -----------------------------------------------
@app.post("/items")
def create_item(item: dict):
    result = collection.insert_one(item)
    return {
        "message": "Manga créé avec succès",
        "id": str(result.inserted_id)
    }


# -----------------------------------------------
# GET /items → Lister tous les mangas
# -----------------------------------------------
@app.get("/items")
def get_all_items(page: int = 1, limit: int = 5):
    skip = (page - 1) * limit          # ex: page 2 → skip 5
    docs = collection.find().skip(skip).limit(limit)
    return [format_doc(d) for d in docs]


# -----------------------------------------------
# GET /items/{id} → Récupérer UN manga par son ID
# -----------------------------------------------
@app.get("/items/{id}")
def get_item(id: str):
    doc = collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Manga introuvable")
    return format_doc(doc)


# -----------------------------------------------
# GET /search → Recherche par mot clé + filtres
# -----------------------------------------------
@app.get("/search")
def search(
    keyword: str = Query(..., description="Mot clé à rechercher"),
    genre: Optional[str] = None,
    note_min: Optional[int] = None
):
    # Recherche sur titre ET description (insensible casse)
    query = {
        "$or": [
            {"titre":       {"$regex": keyword, "$options": "i"}},
            {"description": {"$regex": keyword, "$options": "i"}}
        ]
    }

    # Filtre genre
    if genre:
        query["genre"] = {"$regex": genre, "$options": "i"}

    # Filtre note minimale
    if note_min:
        query["note"] = {"$gte": note_min}

    results = [format_doc(d) for d in collection.find(query)]

    if not results:
        raise HTTPException(status_code=404, detail="Aucun résultat")

    return {"resultats": len(results), "mangas": results}
