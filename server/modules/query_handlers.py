from logger import logger

def query_chain(chain, user_input:str):
    try:

        logger.debug(f"running chain for input: {user_input}")
        result = chain.invoke({"query": user_input})
        response={
            "response":result["result"],
            "sources": [doc.metadata.get("source", "") for doc in result["source_documents"]]
        }
        logger.debug(f"chain response: {response}")
        return response
    
    except Exception as e:
        logger.exception("error on query chain")
        raise