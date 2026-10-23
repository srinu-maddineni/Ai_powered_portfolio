from loader import load_portfolio
from chunker import create_chunks


text = load_portfolio()

chunks = create_chunks(text)

print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print(chunk)