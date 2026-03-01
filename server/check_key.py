import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
print(f"Key loaded: {key[:10]}...")  # shows first 10 chars only
print(f"Key length: {len(key)}")