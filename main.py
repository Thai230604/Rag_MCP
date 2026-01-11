import sys
sys.path.insert(0, "src")
import os
from pathlib import Path
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware as FastAPICORS
from fastmcp import FastMCP
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from dependencies import get_vector_repo, get_chunking_repo
from usecases.ingest_data import IngestDataUseCase
from usecases.retrieve_data import RetrieveDataUseCase
from usecases.chunk_documents import ChunkDocumentsUseCase

# FastAPI app (for Dify and REST clients)
app = FastAPI(title="RAG API", version="1.0.0")

# CORS for FastAPI
app.add_middleware(
    FastAPICORS,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastMCP server (for future MCP clients)
mcp_server = FastMCP("RAG MCP Server")


class RetrieveRequest(BaseModel):
    query: str
    top_k: int = 5


class IngestRequest(BaseModel):
    file_paths: list[str]


# ==================== Core Functions ====================
async def ingest_documents_logic(file_paths: list[str]) -> dict:
    """
    Ingest markdown documents into vector store.
    Documents will be chunked and embedded.
    Provide list of file paths to markdown files.
    """
    # Load documents from file paths
    documents = []
    for file_path in file_paths:
        try:
            path = Path(file_path)
            content = path.read_text(encoding="utf-8")
            
            documents.append({
                "id": path.stem,
                "content": content,
                "metadata": {
                    "source": path.name,
                    "type": "markdown"
                }
            })
        except Exception as e:
            return {"error": f"Failed to read {file_path}: {e}"}
    
    if not documents:
        return {"error": "No documents provided"}
    
    # Initialize repos
    vector_repo = get_vector_repo()
    chunking_repo = get_chunking_repo()
    
    # Chunk documents
    chunk_usecase = ChunkDocumentsUseCase(chunking_repo)
    chunk_result = chunk_usecase.execute(documents)
    
    # Ingest chunks
    ingest_usecase = IngestDataUseCase(vector_repo)
    ingest_result = ingest_usecase.execute(chunk_result['documents'])
    
    return {
        "success": True,
        "files_processed": len(file_paths),
        "original_docs": chunk_result['original_docs'],
        "total_chunks": chunk_result['total_chunks'],
        "chunks_ingested": ingest_result['ingested'],
        "avg_chunks_per_doc": chunk_result['avg_chunks_per_doc']
    }


def retrieve_documents_logic(query: str, top_k: int = 5) -> dict:
    """
    Retrieve relevant documents from vector store.
    """
    # Initialize repo
    vector_repo = get_vector_repo()
    
    # Retrieve
    retrieve_usecase = RetrieveDataUseCase(vector_repo)
    docs = retrieve_usecase.execute(query, top_k)
    
    return {
        "query": query,
        "count": len(docs),
        "results": [
            {
                "content": doc.content,
                "source": doc.metadata.get("source", "unknown"),
                "chunk_index": doc.metadata.get("chunk_index", 0),
                "total_chunks": doc.metadata.get("total_chunks", 1)
            }
            for doc in docs
        ]
    }


# ==================== FastAPI Endpoints (for Dify) ====================
@app.post("/api/v1/ingest")
async def api_ingest(request: IngestRequest) -> dict:
    """REST API: Ingest markdown documents into vector store."""
    return await ingest_documents_logic(request.file_paths)


@app.post("/api/v1/retrieve")
def api_retrieve(request: RetrieveRequest) -> dict:
    """REST API: Retrieve relevant documents from vector store."""
    return retrieve_documents_logic(request.query, request.top_k)


@app.get("/api/v1/health")
def api_health() -> dict:
    """REST API: Check server health."""
    return {"status": "healthy", "service": "RAG API", "qdrant_connected": True}


@app.get("/")
def root():
    """Root endpoint with API info."""
    return {
        "service": "RAG API",
        "version": "1.0.0",
        "endpoints": {
            "ingest": "/api/v1/ingest",
            "retrieve": "/api/v1/retrieve",
            "health": "/api/v1/health",
            "docs": "/docs"
        }
    }


# ==================== FastMCP Tools (for future) ====================
@mcp_server.tool()
async def ingest_documents(file_paths: list[str]) -> dict:
    """MCP Tool: Ingest markdown documents into vector store."""
    return await ingest_documents_logic(file_paths)


@mcp_server.tool()
def retrieve_documents(query: str, top_k: int = 5) -> dict:
    """MCP Tool: Retrieve relevant documents from vector store."""
    return retrieve_documents_logic(query, top_k)


@mcp_server.tool()
def health_check() -> dict:
    """MCP Tool: Check server health."""
    return {"status": "healthy"}


# ==================== Server Runner ====================
def main():
    # Chạy FastAPI server (cho Dify và REST clients)
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting RAG API Server on http://0.0.0.0:{port}")
    print(f"📚 Docs available at http://0.0.0.0:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
