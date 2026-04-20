"""
Bln320 - NoSQL
TP1 - Ex2
MongoDB Atlas découverte
"""

from pathlib import Path
import sys
from pymongo import MongoClient

ROOT = Path(__file__).resolve().parent
while not (ROOT / "DNS.py").exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from DNS import dns

def connect_to_mongodb():
    try: 
        client = MongoClient(dns, ssl=True)
        
        client.server_info()
        print("Connexion réussie à MongoDB Atlas!")
        
        db = client.reseau_social  
        print("Base de données 'reseau_social' prête à l'utilisation")
        
        return db
    except Exception as e:
        print(f"Erreur de connexion à MongoDB Atlas: {e}")
        return None

# Connection
db = connect_to_mongodb()

# Nettoyage pour éviter les doublons si tu relances
db.users.drop()
db.publications.drop()

users = db.users
publications = db.publications

# ============================================================
# Construction du dataset
# ============================================================
# Question 1: insérer 3 utilisateurs et 5 publications (commentaires et likes embarqués dans le document)
users.insert_many([
    {"_id": "user1", "nom": "prenom1",  "age": 28, "ville": "Paris"}, # prenom1
    {"_id": "user2", "nom": "prenom2",    "age": 35, "ville": "Lyon"}, # prenom2
    {"_id": "user3", "nom": "prenom3", "age": 22, "ville": "Marseille"} # prenom3
])
print("3 utilisateurs insérés")

publications.insert_many([
    {"_id": "pub1", "titre": "Publi1",  "auteur_id": "user1", "auteur_nom": "prenom1",   
     "contenu": "Publi1  blabla",                "likes": [], "commentaires": []},
    {"_id": "pub2", "titre": "Publi2",          "auteur_id": "user1", "auteur_nom": "prenom1",   
     "contenu": "Publi2  blabla",          "likes": [], "commentaires": []},
    {"_id": "pub3", "titre": "Publi3",    "auteur_id": "user2", "auteur_nom": "prenom2",     
     "contenu": "Publi3  blabla",         "likes": [], "commentaires": []},
    {"_id": "pub4", "titre": "Publi4",       "auteur_id": "user2", "auteur_nom": "prenom2",     
     "contenu": "Publi4  blabla",            "likes": [], "commentaires": []},
    {"_id": "pub5", "titre": "Publi5",           "auteur_id": "user3", "auteur_nom": "prenom3",  
     "contenu": "Publi5  blabla",   "likes": [], "commentaires": []},
])
print("5 publications insérées\n")

# Question 2: Ajouter des commentaires et des likes sur les publications
# Commentaires sur pub1
publications.update_one(
    {"_id": "pub1"},
    {"$push": {"commentaires": {"auteur": "prenom2", "texte": "Com1 sur Publi1 user2"}}}
)
publications.update_one(
    {"_id": "pub1"},
    {"$push": {"commentaires": {"auteur": "prenom3", "texte": "Com2 sur Publi1 user3"}}}
)

# Commentaires sur pub3
publications.update_one(
    {"_id": "pub3"},
    {"$push": {"commentaires": {"auteur": "prenom1", "texte": "Com1 sur Publi3 user1"}}}
)
publications.update_one(
    {"_id": "pub3"},
    {"$push": {"commentaires": {"auteur": "prenom3", "texte": "Com2 sur Publi3 user3"}}}
)

# Commentaires sur pub5
publications.update_one(
    {"_id": "pub5"},
    {"$push": {"commentaires": {"auteur": "prenom1", "texte": "Com1 sur Publi5 user1"}}}
)
print("Commentaires ajoutés sur pub1, pub3, pub5")

# Likes sur pub1
publications.update_one({"_id": "pub1"}, {"$addToSet": {"likes": "user2"}})
publications.update_one({"_id": "pub1"}, {"$addToSet": {"likes": "user3"}})

# Likes sur pub2
publications.update_one({"_id": "pub2"}, {"$addToSet": {"likes": "user3"}})

# Likes sur pub3
publications.update_one({"_id": "pub3"}, {"$addToSet": {"likes": "user1"}})
publications.update_one({"_id": "pub3"}, {"$addToSet": {"likes": "user3"}})

# Likes sur pub4
publications.update_one({"_id": "pub4"}, {"$addToSet": {"likes": "user1"}})
publications.update_one({"_id": "pub4"}, {"$addToSet": {"likes": "user2"}})
publications.update_one({"_id": "pub4"}, {"$addToSet": {"likes": "user3"}})

print("Likes ajoutés sur pub1, pub2, pub3, pub4")



# ============================================================
# REQUETES
# ============================================================
# Toutes les publications
print("=" * 50)
print("TOUTES LES PUBLICATIONS :")
print("=" * 50)
for pub in publications.find():
    print(f"  [{pub['auteur_nom']}] {pub['titre']}")
    print(f"      {pub['contenu']}")
    print(f"      {len(pub['likes'])} likes | {len(pub['commentaires'])} commentaires\n")

# Publications d'un utilisateur
print("=" * 50)
print("PUBLICATIONS DE prenom1 :")
print("=" * 50)
for pub in publications.find({"auteur_id": "user1"}):
    print(f"  {pub['titre']} - {pub['contenu']}")
print()

# Commentaires d'une publication
print("=" * 50)
print("COMMENTAIRES DE 'Publi1' :")
print("=" * 50)
pub = publications.find_one({"titre": "Publi1"})
if pub["commentaires"]:
    for com in pub["commentaires"]:
        print(f"  [{com['auteur']}] : {com['texte']}")
else:
    print("  Aucun commentaire")
print()

# Publication avec le plus de likes
print("=" * 50)
print("PUBLICATION AVEC LE PLUS DE LIKES :")
print("=" * 50)
top_pub = list(publications.aggregate([
    {
        "$project": {
            "titre": 1,
            "auteur_nom": 1,
            "nb_likes": {"$size": "$likes"}  # calcule la taille du tableau likes
        }
    },
    {"$sort": {"nb_likes": -1}},  # tri décroissant
    {"$limit": 1}                  # on prend le premier
]))
print(f"  {top_pub[0]['titre']} par {top_pub[0]['auteur_nom']} → {top_pub[0]['nb_likes']} likes")
print()

# Nombre de publications par utilisateur
print("=" * 50)
print("NOMBRE DE PUBLICATIONS PAR UTILISATEUR :")
print("=" * 50)
stats = publications.aggregate([
    {
        "$group": {
            "_id": "$auteur_nom",           # on regroupe par auteur
            "nb_publications": {"$sum": 1}  # on compte
        }
    },
    {"$sort": {"nb_publications": -1}}
])
for stat in stats:
    print(f"  {stat['_id']} → {stat['nb_publications']} publication(s)")
