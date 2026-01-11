# usecases/ingest_data.py
from domain.entities.document import Document
from domain.ports.vector_repository import VectorRepository

class IngestDataUseCase:

    def __init__(self, vector_repo: VectorRepository):
        self.vector_repo = vector_repo

    def execute(self, raw_docs: list[dict]):
        documents = [
            Document(
                doc_id=d["id"],
                content=d["content"],
                metadata=d.get("metadata", {})
            )
            for d in raw_docs
        ]

        self.vector_repo.upsert(documents)
        return {"ingested": len(documents)}
