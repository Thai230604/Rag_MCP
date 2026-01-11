# usecases/retrieve_data.py
from domain.ports.vector_repository import VectorRepository

class RetrieveDataUseCase:

    def __init__(self, vector_repo: VectorRepository):
        self.vector_repo = vector_repo

    def execute(self, query: str, top_k: int = 5):
        return self.vector_repo.search(query, top_k)
