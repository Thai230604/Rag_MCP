from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from domain.entities.document import Document
from domain.ports.vector_repository import VectorRepository


class QdrantRepository(VectorRepository):

    def __init__(self, client: QdrantClient, collection_name: str, embeddings):
        self.client = client
        self.collection = collection_name
        self.embeddings = embeddings

    def upsert(self, documents: list[Document]):
        """Upsert documents to Qdrant"""
        contents = [d.content for d in documents]
        vectors = self.embeddings.embed_documents(contents)

        points = [
            PointStruct(
                id=int(d.doc_id) if d.doc_id.isdigit() else hash(d.doc_id) % (10 ** 8),
                vector=vector,
                payload={"content": d.content, **(d.metadata or {})}
            )
            for i, (d, vector) in enumerate(zip(documents, vectors))
        ]

        self.client.upsert(
            collection_name=self.collection,
            points=points
        )

    def search(self, query: str, top_k: int) -> list[Document]:
        """Search for documents in Qdrant"""
        vector = self.embeddings.embed_query(query)

        hits = self.client.query_points(
            collection_name=self.collection,
            query=vector,
            limit=top_k
        )

        return [
            Document(
                doc_id=str(hit.id),
                content=hit.payload["content"],
                metadata={k: v for k, v in hit.payload.items() if k != "content"}
            )
            for hit in hits.points
        ]
