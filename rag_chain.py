from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
import os

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

llm = OllamaLLM(
    model="llama3"
)

def ask_question(question):

    docs = vectorstore.similarity_search(
        question,
        k=3
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a Data Science Interview Assistant.

Answer the question using the context below.

Context:
{context}

Question:
{question}

Answer:
"""

    answer = llm.invoke(prompt)

    sources = []

    for doc in docs:

        source = os.path.basename(
            doc.metadata.get(
                "source",
                "Unknown"
            )
        )

        sources.append(source)

    sources = list(set(sources))

    return answer, sources, docs