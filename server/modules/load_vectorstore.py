import os
import time
from pathlib import Path
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "medicalindex"

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Moved outside function — loads model once, not on every request
embed_model = HuggingFaceEmbeddings(
    model_name="all-mpnet-base-v2",        # 768 dimensions — matches Pinecone
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud="aws", region=PINECONE_ENV)

existing_indexes = [i.name for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=768,                     # matches all-mpnet-base-v2
        metric="dotproduct",
        spec=spec
    )
    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pc.Index(PINECONE_INDEX_NAME)


def load_vectorstore(uploaded_files):
    file_paths = []

    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR) / file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        file_paths.append(str(save_path))

    for path in file_paths:
        loader = PyPDFLoader(path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadatas = [
            {**chunk.metadata, "text": chunk.page_content}
            for chunk in chunks
        ]

        file_stem = Path(path).stem
        ids = [f"{file_stem}-{i}" for i in range(len(chunks))]

        print(f"Embedding {len(texts)} chunks for {file_stem}...")
        embeddings = embed_model.embed_documents(texts)

        vectors_to_upsert = list(zip(ids, embeddings, metadatas))

        print("Upserting to Pinecone...")
        index.upsert(vectors=vectors_to_upsert)

        print(f"✅ Upload complete for {path}")