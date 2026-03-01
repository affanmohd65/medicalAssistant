import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAIEmbeddings

models_to_try = [
    "models/embedding-001",
    "models/text-embedding-004",
    "text-embedding-004",
    "embedding-001",
]

for model in models_to_try:
    try:
        embed = GoogleGenerativeAIEmbeddings(
            model=model,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        result = embed.embed_query("test")
        print(f"✅ WORKS: {model} — vector size: {len(result)}")
    except Exception as e:
        print(f"❌ FAILED: {model} — {str(e)[:80]}")