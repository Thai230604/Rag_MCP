"""Dependency injection for RAG system"""
import sys
sys.path.insert(0, "src")

from core.config import settings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_openai import OpenAIEmbeddings
from infrastructure.qdrant_repository import QdrantRepository
from infrastructure.chunking_repository import MarkdownChunkingRepository


def get_embeddings():
    """Get OpenAI embeddings"""
    return OpenAIEmbeddings(
        api_key=settings.openai_api_key,
        model=settings.embedding_model
    )


def get_qdrant_client():
    """Get Qdrant client"""
    return QdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        api_key=settings.qdrant_api_key,
        prefer_grpc=False,
        https=False
    )


def ensure_collection():
    """Ensure collection exists in Qdrant"""
    client = get_qdrant_client()
    try:
        client.get_collection(settings.qdrant_collection)
    except Exception:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=settings.embedding_dim,
                distance=Distance.COSINE
            )
        )


def get_vector_repo():
    """Get vector repository instance"""
    ensure_collection()
    embeddings = get_embeddings()
    client = get_qdrant_client()
    return QdrantRepository(client, settings.qdrant_collection, embeddings)


def get_chunking_repo():
    """Get chunking repository instance"""
    return MarkdownChunkingRepository(chunk_size=1000, chunk_overlap=0)
