from pymongo import MongoClient

dns = "mongodb+srv://adriennitot_db_user:XkZhru4IAE7E3I5z@cluster0.u6zu3vs.mongodb.net/?appName=Cluster0"

def test_connect_to_mongodb():
    try: 
        client = MongoClient(dns, ssl=True)
        
        client.server_info()
        print("Connexion réussie à MongoDB Atlas!")
        
        db = client.ecommerce  # ✅ Changement ici
        print("Base de données 'ecommerce' prête à l'utilisation")
        
        return db
    except Exception as e:
        print(f"Erreur de connexion à MongoDB Atlas: {e}")
        return None

