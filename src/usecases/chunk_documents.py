"""Chunk documents usecase"""
from domain.ports.chunking_repository import ChunkingRepository


class ChunkDocumentsUseCase:
    """Usecase for chunking documents"""

    def __init__(self, chunking_repo: ChunkingRepository):
        self.chunking_repo = chunking_repo

    def execute(self, documents: list[dict]) -> dict:
        """Execute chunking
        
        Args:
            documents: List of dicts with 'id', 'content', 'metadata'
        
        Returns:
            Dict with chunking statistics
        """
        chunked_docs = self.chunking_repo.chunk_documents(documents)

        # Calculate statistics
        total_chunks = len(chunked_docs)
        original_size = sum(len(doc.get("content", "")) for doc in documents)
        chunked_size = sum(len(doc.get("content", "")) for doc in chunked_docs)

        return {
            "original_docs": len(documents),
            "total_chunks": total_chunks,
            "original_size": original_size,
            "chunked_size": chunked_size,
            "avg_chunks_per_doc": total_chunks / len(documents) if documents else 0,
            "documents": chunked_docs
        }
