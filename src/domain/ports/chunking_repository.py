"""Chunking repository interface"""
from abc import ABC, abstractmethod


class ChunkingRepository(ABC):
    """Abstract repository for document chunking"""

    @abstractmethod
    def chunk_text(self, text: str) -> list[str]:
        """Chunk single text document"""
        pass

    @abstractmethod
    def chunk_documents(self, documents: list[dict]) -> list[dict]:
        """Chunk multiple documents
        
        Args:
            documents: List of dicts with 'id', 'content', 'metadata'
        
        Returns:
            List of dicts with 'id', 'content', 'metadata', 'chunk_index'
        """
        pass
