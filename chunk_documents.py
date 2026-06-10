from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.load_documents import load_documents

def chunk_documents():

    docs = load_documents()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    return chunks


if __name__ == "__main__":
    chunks = chunk_documents()
    print(f"Created {len(chunks)} chunks")