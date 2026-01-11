from pydantic import BaseModel, Field
from typing import Optional


class Document(BaseModel):
    doc_id: str = Field(..., description="Unique document ID")
    content: str = Field(..., description="Document content")
    metadata: Optional[dict] = Field(default_factory=dict, description="Document metadata")
    
    class Config:
        arbitrary_types_allowed = True
