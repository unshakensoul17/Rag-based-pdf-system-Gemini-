import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000/api/v1"
API_KEY = os.getenv("API_AUTH_KEY", "your-secret-api-key-for-client-auth")
PDF_PATH = "/home/unshakensoul/Downloads/krishnapal.pdf"

headers = {
    "X-API-Key": API_KEY
}

def ingest_and_chat():
    print(f"Uploading {PDF_PATH}...")
    
    if not os.path.exists(PDF_PATH):
        print(f"❌ File not found: {PDF_PATH}")
        return

    files = {'file': open(PDF_PATH, 'rb')}
    
    try:
        # 1. Ingest
        response = requests.post(f"{API_URL}/ingest", headers=headers, files=files)
        if response.status_code == 200:
            print(f"✅ Ingestion Successful!")
            print(f"Server Response: {response.json()}")
        else:
            print(f"❌ Ingestion Failed: {response.text}")
            return

        # 2. Query
        question = "Summarize this document in 2 sentences."
        print(f"\nAsking: '{question}'...")
        
        query_payload = {"query": question, "limit": 3}
        response = requests.post(f"{API_URL}/query", headers=headers, json=query_payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Answer Received:")
            print(f"---\n{data['answer']}\n---")
        else:
            print(f"❌ Query Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    ingest_and_chat()
