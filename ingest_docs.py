import sys
sys.path.insert(0, "src")

import os
from pathlib import Path
from dependencies import get_vector_repo
from usecases.ingest_data import IngestDataUseCase

def ingest_markdown_files():
    """Ingest all markdown files from doc folder"""
    doc_folder = Path("doc")
    vector_repo = get_vector_repo()
    usecase = IngestDataUseCase(vector_repo)
    
    documents = []
    
    # Read all markdown files
    for i, md_file in enumerate(sorted(doc_folder.glob("*.md")), 1):
        try:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            documents.append({
                "id": str(i),
                "content": content,
                "metadata": {
                    "source": md_file.name,
                    "type": "markdown"
                }
            })
            print(f"✓ Read {md_file.name} ({len(content)} chars)")
        except Exception as e:
            print(f"✗ Error reading {md_file.name}: {e}")
    
    if documents:
        print(f"\n📝 Ingesting {len(documents)} documents...")
        result = usecase.execute(documents)
        print(f"✅ {result['ingested']} documents ingested to Qdrant\n")
        
        # List ingested files
        print("Ingested files:")
        for doc in documents:
            print(f"  - {doc['metadata']['source']}")
    else:
        print("No markdown files found in doc folder")

if __name__ == "__main__":
    ingest_markdown_files()
