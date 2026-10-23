from langchain_text_splitters import RecursiveCharacterTextSplitter
# from loader import load_portfolio
# text = load_portfolio()

def create_chunks(text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=[
            "\n## ",
            "\n### ",
            "\n\n",
            "\n",
            " ",
            ""
        ]
    )

    chunks = splitter.split_text(text)


    return chunks
