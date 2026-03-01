from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain.schema import BaseRetriever
from langchain_huggingface import HuggingFaceEmbeddings  # ✅ changed
from pinecone import Pinecone
from pydantic import Field
from typing import List, Optional
from logger import logger
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

#Initialize once - not inside the route
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))         
index = pc.Index(os.getenv("PINECONE_INDEX_NAME", "medicalindex"))  

embed_model = HuggingFaceEmbeddings(           #no API key needed
    model_name="all-mpnet-base-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)


class SimpleRetriever(BaseRetriever):          # moved outside route
    docs: List[Document] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str) -> List[Document]:
        return self.docs


@router.post("/ask")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"User query: {question}")

        embedded_query = embed_model.embed_query(question)
        res = index.query(vector=embedded_query, top_k=3, include_metadata=True)

        docs = [
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
            )
            for match in res["matches"]
        ]

        retriever = SimpleRetriever(docs=docs)
        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)

        logger.info("Query successful")
        return result

    except Exception as e:
        logger.exception("Error while processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})