import sys
sys.path.insert(0, "src")

from dependencies import get_qdrant_client
from core.config import settings

# Get client
client = get_qdrant_client()

# List collections
collections = client.get_collections()
print("Collections:")
for collection in collections.collections:
    print(f"  - {collection.name}")

# Get collection info
try:
    collection_info = client.get_collection(settings.qdrant_collection)
    print(f"\nCollection: {settings.qdrant_collection}")
    print(f"  Points: {collection_info.points_count}")
    print(f"  Vectors: {collection_info.config.params.vectors.size}")
    
    # Get all points
    points = client.scroll(settings.qdrant_collection, limit=100)
    print(f"\nStored documents ({len(points[0])}):")
    for point in points[0]:
        print(f"  ID: {point.id}")
        print(f"    Content: {point.payload.get('content', '')[:60]}...")
        print()
except Exception as e:
    print(f"Error: {e}")
