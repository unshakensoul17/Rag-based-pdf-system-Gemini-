import requests
import os
from fpdf import FPDF
from dotenv import load_dotenv

load_dotenv()

API_URL = "http://localhost:8000/api/v1"
API_KEY = os.getenv("API_AUTH_KEY", "your-secret-api-key-for-client-auth")

headers = {
    "X-API-Key": API_KEY
}

def test_health():
    print("Testing Health Check...")
    try:
        response = requests.get(f"http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health Check Passed")
        else:
            print(f"❌ Health Check Failed: {response.text}")
    except Exception as e:
        print(f"❌ Health Check Failed: {e}")

def test_ingest_and_query():
    print("\nTesting Ingestion...")
    # Create a dummy PDF file
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="This is a test document for the RAG system.", ln=1, align="C")
    pdf.cell(200, 10, txt="The capital of France is Paris.", ln=2, align="L")
    pdf.cell(200, 10, txt="FastAPI is a modern, fast (high-performance), web framework for building APIs with Python.", ln=3, align="L")
    pdf.output("test_doc.pdf")
    
    files = {'file': open('test_doc.pdf', 'rb')}
    
    try:
        response = requests.post(f"{API_URL}/ingest", headers=headers, files=files)
        if response.status_code == 200:
            print(f"✅ Ingestion Passed: {response.json()}")
            doc_id = response.json().get("document_id")
        else:
            print(f"❌ Ingestion Failed: {response.text}")
            return
            
        print("\nTesting Query...")
        query_payload = {"query": "What is the capital of France?", "limit": 3}
        response = requests.post(f"{API_URL}/query", headers=headers, json=query_payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Query Passed.")
            print(f"Answer: {data['answer']}")
            print(f"Sources: {[s['content'][:50] for s in data['sources']]}")
        else:
            print(f"❌ Query Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Test Failed: {e}")
    finally:
        if os.path.exists("test_doc.pdf"):
            os.remove("test_doc.pdf")

if __name__ == "__main__":
    test_health()
    test_ingest_and_query()
