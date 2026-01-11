"""Chunking repository implementation"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from domain.ports.chunking_repository import ChunkingRepository


class MarkdownChunkingRepository(ChunkingRepository):
    """Chunking repository for markdown documents"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 0):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n## ",
                "\n### ",
                "\n#### ",
                "\n\n",
                "\n",
                " ",
                ""
            ]
        )

    def chunk_text(self, text: str) -> list[str]:
        """Chunk single text document"""
        return self.splitter.split_text(text)

    def chunk_documents(self, documents: list[dict]) -> list[dict]:
        """Chunk multiple documents"""
        chunked_docs = []

        for doc in documents:
            content = doc.get("content", "")
            doc_id = doc.get("id")
            metadata = doc.get("metadata", {})

            # Chunk the content
            chunks = self.chunk_text(content)

            # Create chunked documents
            for chunk_idx, chunk_content in enumerate(chunks):
                chunked_docs.append({
                    "id": f"{doc_id}_chunk_{chunk_idx}",
                    "content": chunk_content,
                    "metadata": {
                        **metadata,
                        "source_doc_id": doc_id,
                        "chunk_index": chunk_idx,
                        "total_chunks": len(chunks)
                    }
                })

        return chunked_docs
