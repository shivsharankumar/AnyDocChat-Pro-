from langchain_community.vectorstores import Chroma,FAISS
# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


from typing import List


def create_faiss_index(texts: List[str], embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """Create a FAISS vector store from the provided texts."""
    #model_name="sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
    vector_store = FAISS.from_texts(texts, embeddings)
    return vector_store

def retrive_relevant_docs_faiss(vector_store: FAISS, query: str, k: int = 4):
    """Retrieve relevant documents from the FAISS vector store based on the query."""
    docs = vector_store.similarity_search(query, k=k)
    return docs