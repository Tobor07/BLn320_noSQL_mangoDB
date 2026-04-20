"""
Bln320 - NoSQL
TP1 - Ex1
MongoDB Atlas découverte
"""

from pymongo import MongoClient

dns = "mongodb+srv://adriennitot_db_user:cle@cluster0.u6zu3vs.mongodb.net/?appName=Cluster0"

def connect_to_mongodb():
    try: 
        client = MongoClient(dns, ssl=True)
        
        client.server_info()
        print("Connexion réussie à MongoDB Atlas!")
        
        db = client.ecommerce  
        print("Base de données 'ecommerce' prête à l'utilisation")
        
        return db
    except Exception as e:
        print(f"Erreur de connexion à MongoDB Atlas: {e}")
        return None

# Question 1: Connectez-vous à MongoDB Atlas et affichez les bases de données disponibles.
db = connect_to_mongodb()


# Question 2: Créez une collection "products" dans la base de données "ecommerce" et insérez un document représentant un produit (users, products, orders).
users= db.users
products = db.products
orders = db.orders


# Question 3: Insérez des documents dans les collections
#Création de 3 utilisateurs
users.insert_many([
    {"nom": "Alice Dupont",  "age": 28, "ville": "Paris"},
    {"nom": "Bob Martin",    "age": 35, "ville": "Lyon"},
    {"nom": "Clara Bernard", "age": 22, "ville": "Paris"}
])
print("3 utilisateurs insérés")

products.insert_many([
    {"nom": "Laptop",      "prix": 999,  "categorie": "Informatique"},
    {"nom": "Souris",      "prix": 29,   "categorie": "Informatique"},
    {"nom": "Casque Audio","prix": 79,   "categorie": "Audio"},
    {"nom": "Clavier",     "prix": 49,   "categorie": "Informatique"}
])
print(" 4 produits insérés")

orders.insert_one({
    "utilisateur": "Alice Dupont",
    "produits": [
        {"nom": "Laptop",       "prix": 999},
        {"nom": "Casque Audio", "prix": 79}
    ],
    "total": 1078
})
print("1 commande insérée\n")


# Question 4: Affichez tous les utilisateurs de la collection "users" et tous les produits de la collection "products".
print("Tous les utilisateurs :")
for user in users.find():
    print(f"  - {user['nom']} | {user['age']} ans | {user['ville']}")
print()

# Produits dont le prix > 50
print("Produits avec prix > 50 :")
for product in products.find({"prix": {"$gt": 50}}):
    print(f"  - {product['nom']} | {product['prix']}€ | {product['categorie']}")
print()

# Utilisateurs habitant à Paris
print("Utilisateurs habitant à Paris :")
for user in users.find({"ville": "Paris"}):
    print(f"  - {user['nom']} | {user['age']} ans")
print()

# Toutes les commandes
print("Toutes les commandes :")
for order in orders.find():
    print(f"  - Client : {order['utilisateur']} | Total : {order['total']}€")
    for p in order["produits"]:
        print(f"      • {p['nom']} - {p['prix']}€")
print()


# Question 5: Mettez à jour l'âge d'un utilisateur 
users.update_one(
    {"nom": "Bob Martin"},   # filtre
    {"$set": {"age": 40}}    # modification
)
print("Âge de Bob Martin mis à jour")

# Vérification
bob = users.find_one({"nom": "Bob Martin"})
print(f"Nouvel âge : {bob['age']} ans\n")

# Question 6: Supprimez un produit de la collection "products"
products.delete_one({"nom": "Souris"})
print("Produit 'Souris' supprimé")

# Vérification
print("Produits restants :")
for product in products.find():
    print(f"  - {product['nom']} | {product['prix']}€")
