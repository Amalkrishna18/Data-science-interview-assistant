from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from src.chunk_documents import chunk_documents


def create_vectorstore():

    print("Loading and chunking documents...")

    chunks = chunk_documents()

    print(f"Total chunks: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="vectorstore"
    )

    print("Vector database created successfully!")


if __name__ == "__main__":
    create_vectorstore()