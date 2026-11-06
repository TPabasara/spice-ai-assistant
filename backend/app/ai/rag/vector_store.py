import os
import chromadb
from typing import List, Dict, Any
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

class ChromaDBManager:
    """
    Manages vector embeddings and semantic search using ChromaDB and Google Embeddings.
    """
    def __init__(self, persist_directory: str = None):
        # Dynamically set path: Use environment variable in production (Render), fallback to WSL path locally
        if persist_directory is None:
            persist_directory = os.getenv("CHROMA_DB_PATH", "/home/tharindu/spice_chroma_db")

        # Initialize Google Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GOOGLE_API_KEY
        )
        
        # Initialize persistent ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create the collection for our documents
        self.collection = self.client.get_or_create_collection(
            name="spice_assistant_docs",
            metadata={"hnsw:space": "cosine"} # Cosine similarity is best for text
        )

    def add_documents(self, chunks: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
        """
        Generates embeddings for text chunks and stores them in ChromaDB.
        """
        if not chunks:
            return
            
        # LangChain's embedding wrapper handles the API calls to Google
        embeddings_list = self.embeddings.embed_documents(chunks)
        
        self.collection.add(
            embeddings=embeddings_list,
            documents=chunks,
            metadatas=metadatas,
            ids=ids
        )

    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Embeds the user query and finds the most semantically similar chunks.
        """
        query_embedding = self.embeddings.embed_query(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results into a cleaner structure for the LangGraph agent
        formatted_results = []
        if results['documents'] and len(results['documents'][0]) > 0:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": results['distances'][0][i] if 'distances' in results else None
                })
                
        return formatted_results