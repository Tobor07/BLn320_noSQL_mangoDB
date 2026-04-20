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
        
        db = client.reseau_social  # ✅ Changement ici
        print("Base de données 'reseau_social' prête à l'utilisation")
        
        return db
    except Exception as e:
        print(f"Erreur de connexion à MongoDB Atlas: {e}")
        return None
