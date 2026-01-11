# domain/ports/vector_repository.py
from abc import ABC, abstractmethod
from domain.entities.document import Document

class VectorRepository(ABC):

    @abstractmethod
    def upsert(self, documents: list[Document]):
        pass

    @abstractmethod
    def search(self, query: str, top_k: int) -> list[Document]:
        pass
