"""
Bln320 - NoSQL
TP1 - Ex2
MongoDB Atlas découverte
"""

from pymongo import MongoClient

dns = "mongodb+srv://adriennitot_db_user:XkZhru4IAE7E3I5z@cluster0.u6zu3vs.mongodb.net/?appName=Cluster0"

def connect_to_mongodb():
    try: 
        client = MongoClient(dns, ssl=True)
        
        client.server_info()
        print("Connexion réussie à MongoDB Atlas!")
        
        db = client.reseau_social  # ✅ Changement ici
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
    {"_id": "user1", "nom": "Alice Dupont",  "age": 28, "ville": "Paris"},
    {"_id": "user2", "nom": "Bob Martin",    "age": 35, "ville": "Lyon"},
    {"_id": "user3", "nom": "Clara Bernard", "age": 22, "ville": "Marseille"}
])
print("3 utilisateurs insérés")

publications.insert_many([
    {"_id": "pub1", "titre": "Ma première publication",  "auteur_id": "user1", "auteur_nom": "Alice Dupont",   
     "contenu": "Bonjour tout le monde ! 👋",                "likes": [], "commentaires": []},
    {"_id": "pub2", "titre": "Recette du jour",          "auteur_id": "user1", "auteur_nom": "Alice Dupont",   
     "contenu": "Aujourd'hui je fais une quiche 🥧",          "likes": [], "commentaires": []},
    {"_id": "pub3", "titre": "Randonnée en montagne",    "auteur_id": "user2", "auteur_nom": "Bob Martin",     
     "contenu": "Superbe journée dans les Alpes 🏔️",         "likes": [], "commentaires": []},
    {"_id": "pub4", "titre": "Concert incroyable",       "auteur_id": "user2", "auteur_nom": "Bob Martin",     
     "contenu": "Soirée inoubliable hier soir 🎵",            "likes": [], "commentaires": []},
    {"_id": "pub5", "titre": "Nouvelle ville",           "auteur_id": "user3", "auteur_nom": "Clara Bernard",  
     "contenu": "Je viens de m'installer à Bordeaux ! 🏙️",   "likes": [], "commentaires": []},
])
print("5 publications insérées\n")

# Question 2: Ajouter des commentaires et des likes sur les publications
# Commentaires sur pub1
publications.update_one(
    {"_id": "pub1"},
    {"$push": {"commentaires": {"auteur": "Bob Martin", "texte": "Bienvenue Alice !"}}}
)
publications.update_one(
    {"_id": "pub1"},
    {"$push": {"commentaires": {"auteur": "Clara Bernard", "texte": "Hello ! 😊"}}}
)

# Commentaires sur pub3
publications.update_one(
    {"_id": "pub3"},
    {"$push": {"commentaires": {"auteur": "Alice Dupont", "texte": "Trop beau !"}}}
)
publications.update_one(
    {"_id": "pub3"},
    {"$push": {"commentaires": {"auteur": "Clara Bernard", "texte": "Je veux y aller 😍"}}}
)

# Commentaires sur pub5
publications.update_one(
    {"_id": "pub5"},
    {"$push": {"commentaires": {"auteur": "Alice Dupont", "texte": "Bordeaux c'est super !"}}}
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
print("📋 TOUTES LES PUBLICATIONS :")
print("=" * 50)
for pub in publications.find():
    print(f"  📝 [{pub['auteur_nom']}] {pub['titre']}")
    print(f"      {pub['contenu']}")
    print(f"      ❤️  {len(pub['likes'])} likes | 💬 {len(pub['commentaires'])} commentaires\n")

# Publications d'un utilisateur
print("=" * 50)
print("👤 PUBLICATIONS DE Alice Dupont :")
print("=" * 50)
for pub in publications.find({"auteur_id": "user1"}):
    print(f"  📝 {pub['titre']} - {pub['contenu']}")
print()

# Commentaires d'une publication
print("=" * 50)
print("💬 COMMENTAIRES DE 'Ma première publication' :")
print("=" * 50)
pub = publications.find_one({"titre": "Ma première publication"})
if pub["commentaires"]:
    for com in pub["commentaires"]:
        print(f"  [{com['auteur']}] : {com['texte']}")
else:
    print("  Aucun commentaire")
print()

# 4Publication avec le plus de likes (aggregation)
print("=" * 50)
print("🏆 PUBLICATION AVEC LE PLUS DE LIKES :")
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
print(f"  🥇 {top_pub[0]['titre']} par {top_pub[0]['auteur_nom']} → {top_pub[0]['nb_likes']} likes")
print()

# Nombre de publications par utilisateur (aggregation)
print("=" * 50)
print("📊 NOMBRE DE PUBLICATIONS PAR UTILISATEUR :")
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
    print(f"  👤 {stat['_id']} → {stat['nb_publications']} publication(s)")
