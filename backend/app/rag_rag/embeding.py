import chromadb
from .chunker import create_chunks
from .loader import load_portfolio


client = chromadb.PersistentClient(path=r"C:\Users\srinu\OneDrive\Desktop\rag\backend\data\croma")

# Get or create collection — only index if it's empty (skips on every restart unless collection is wiped)
collection = client.get_or_create_collection(name="my_collection")

if collection.count() == 0:
    text = load_portfolio()
    chunks = create_chunks(text)
    collection.add(
        documents=chunks,
        ids=[f"doc{i}" for i in range(len(chunks))]
    )
    print(f"[embeding] Indexed {collection.count()} chunks into collection.")
else:
    print(f"[embeding] Collection already has {collection.count()} chunks. Skipping re-index.")


def query(text: str):
    result = collection.query(
        query_texts=[text],
        n_results=5
    )
    return result
