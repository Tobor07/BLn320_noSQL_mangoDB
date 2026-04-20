"""
Bln320 - NoSQL
partiel - Exo
MongoDB
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
        
        db = client.appli_web
        print("Base de données 'appli_web' prête à l'utilisation")
        
        return db
    except Exception as e:
        print(f"Erreur de connexion à MongoDB Atlas: {e}")
        return None


# I - Connection à MongoDB Atlas et création de la base de données et des collections
db = connect_to_mongodb()

"""
users= db.users
users.delete_many({})  # pour vider la collection


# II - Requêtes de base
# 1-) On insère des documents dans la collection "users"
users.insert_many([
    {"nom": "user1", "mail": 
     "user1@example.com", 
     "addresse": ["u1_address1", "u1_address2"],
     "notifications": {"email": True, "sms": False}},
    {"nom": "user2", 
     "mail": "user2@example.com", 
     "addresse": ["u2_address1"],
     "notifications": {"email": False, "sms": True}},
    {"nom": "user4", 
     "mail": "user4@example.com",
     "addresse": ["u4_address1", "u4_address2", "u4_address3"],
     "notifications": {"email": True, "sms": True}},
    {"nom": "user3", 
     "mail": "user3@example.com",
     "notifications": {"email": False, "sms": False}}
])
print("\n4 utilisateurs insérés")

# 2-) Lecture de tous les documents de la collection "users"
print("\nTous les utilisateurs :")
for user in users.find():
    print(f"  - {user['nom']} | {user['mail']} | {user.get('addresse', 'Pas d\'adresse')} | Notifications: {user['notifications']}")
print()

# 3-) Update d'un document : on modifie les notifications de user3
users.update_one(
    {"nom": "user3"},  
    {"$set": {"notifications.email": True, "notifications.sms": True}}  
)
print("Notifications de user3 mises à jour :")
for user in users.find({"nom": "user3"}):
    print(f"{user['nom']} | {user['notifications']}")
print()

# 4-) Suppression d'un document : on supprime user2
users.delete_one({"nom": "user2"})
print("Utilisateur 'user2' supprimé.")
liste_users = []
for user in users.find():
   liste_users.append(f"{user['nom']}")
print("Utilisateurs restants : ", liste_users)
print()


# III - Requêtes avancées
# 1-) Filtage avancé : Récupérez les utilisateurs ayant activé les notifications et possédant plusieurs adresses.
print("Utilisateurs avec notifications activées et plusieurs adresses :")
for user in users.find({"notifications.email": True, "notifications.sms": True, "addresse.1": {"$exists": True}}):
    print(f"  - {user['nom']} | {user['addresse']} | Notifications: {user['notifications']}")
print()


# 2-) Tri et projection : Affichez les utilisateurs triés par nom sans afficher certains champs 
print("Utilisateurs triés par nom :")
for user in users.find({}, {"nom": 1, "mail": 1, "_id": 0}).sort("nom", 1):
    print(f"  - {user['nom']} | {user['mail']}")
print()


# 3-) Mise à jour conditionnelle : Ajoutez un attribut (ex : “premium”) uniquement aux utilisateurs répondant à une condition (ex : nombre de commandes élevé)
print("Ajout de l'attribut 'premium' aux utilisateurs avec plus de 2 adresses :")
users.update_many(
    {"addresse.2": {"$exists": True}},  
    {"$set": {"premium": True}}  
)
for user in users.find({"premium": True}):
    print(f"  - {user['nom']} | Premium: {user['premium']} | Adresses: {user['addresse']}")"""
