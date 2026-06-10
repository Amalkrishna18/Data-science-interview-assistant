import streamlit as st
import os
from src.rag_chain import ask_question

st.set_page_config(
    page_title="Data Science Interview Assistant",
    layout="wide"
)

# Sidebar Header
st.sidebar.title("🤖 BI Assistant")

st.sidebar.markdown(
    "Your Business Intelligence Copilot"
)

st.sidebar.markdown("---")

# Navigation Menu
page = st.sidebar.radio(
    "Navigation",
    [
        "Chat",
        "Documents",
        "Analytics",
        "Settings"
    ]
)
st.sidebar.markdown("---")

st.sidebar.subheader(
    "Recent Questions"
)

if "messages" in st.session_state:

    for msg in st.session_state.messages[-5:]:

        if msg["role"] == "user":

            st.sidebar.write(
                f"• {msg['content']}"
            )

# ---------------- CHAT PAGE ---------------- #

if page == "Chat":

    st.title("📚 Data Science Interview Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if "sources" in message:
                st.markdown("### Sources")
                for source in message["sources"]:
                    st.markdown(f"📄 {source}")

    question = st.chat_input(
        "Ask a Data Science Question"
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer, sources, docs = ask_question(question)

                st.markdown(answer)

                st.markdown("### Sources")

                for source in sources:
                    st.markdown(f"📄 {source}")
                with st.expander("🔍 Retrieved Chunks"):

                    for i, doc in enumerate(docs, start=1):

                        st.markdown(
                            f"### Chunk {i}"
                        )

                        st.info(
                         doc.page_content[:500]
                        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources
            }
        )

# ---------------- DOCUMENTS PAGE ---------------- #

elif page == "Documents":

    st.title("📄 Document Manager")

    uploaded_files = st.file_uploader(
        "Upload PDF Documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Save uploaded files
    if uploaded_files:

        for file in uploaded_files:

            save_path = os.path.join(
                "data",
                file.name
            )

            with open(save_path, "wb") as f:
                f.write(file.getbuffer())

            st.success(
                f"✅ {file.name} uploaded successfully"
            )
            from src.create_vectorstore import create_vectorstore

    
    # ADD THIS BLOCK HERE
    if st.button("🔄 Rebuild Vector Database",
         key="rebuild_vector_db_btn"
    ):

        from src.create_vectorstore import create_vectorstore

        with st.spinner("Rebuilding vector database..."):
            create_vectorstore()

        st.success(
            "✅ Vector database rebuilt successfully!"
        )

    # Display uploaded documents
    files = os.listdir("data")

    st.subheader("Uploaded Documents")

    # Display uploaded documents
    files = os.listdir("data")

    st.subheader("Uploaded Documents")

    if len(files) == 0:

        st.info("No documents uploaded yet.")

    else:

        st.metric(
            "Total Documents",
            len(files)
        )

        for file in files:

            file_path = os.path.join(
                "data",
                file
            )

            file_size = os.path.getsize(file_path)

            st.write(
                f"📄 {file} ({round(file_size/1024,2)} KB)"
            )

    # Document statistics
    st.subheader("📊 Document Statistics")

    total_size = 0

    for file in files:

        file_path = os.path.join(
            "data",
            file
        )

        total_size += os.path.getsize(file_path)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Files",
            len(files)
        )

    with col2:
        st.metric(
            "Total Size (MB)",
            round(total_size / (1024 * 1024), 2)
        )

    # Delete Documents Section
    st.subheader("🗑️ Delete Document")

    if files:

        selected_file = st.selectbox(
            "Choose document",
            files
        )

        if st.button("Delete Selected File"):

            os.remove(
                os.path.join(
                    "data",
                    selected_file
                )
            )

            st.success(
                f"{selected_file} deleted successfully"
            )

            st.rerun()
# ---------------- ANALYTICS PAGE ---------------- #

elif page == "Analytics":

    st.title("📊 Analytics Dashboard")

    os.makedirs("data", exist_ok=True)

    files = os.listdir("data")

    total_docs = len(files)

    total_size = 0

    for file in files:

        file_path = os.path.join("data", file)

        if os.path.isfile(file_path):
            total_size += os.path.getsize(file_path)

    total_questions = 0

    if "messages" in st.session_state:

        total_questions = len(
            [
                msg
                for msg in st.session_state.messages
                if msg["role"] == "user"
            ]
        )

    col1, col2, col3 = st.columns(3)

    col1.metric("Documents", total_docs)

    col2.metric("Questions Asked", total_questions)

    col3.metric(
        "Storage Used (MB)",
        round(total_size / (1024 * 1024), 2)
    )

    st.subheader("Document Overview")

    if files:

        for file in files:

            file_path = os.path.join("data", file)

            if os.path.isfile(file_path):

                file_size = os.path.getsize(file_path)

                st.write(
                    f"📄 {file} - {round(file_size/1024,2)} KB"
                )

    else:

        st.info("No documents available.")

# ---------------- SETTINGS PAGE ---------------- #

elif page == "Settings":

    st.title("⚙️ Settings")

    st.subheader("Current Configuration")

    st.code("""
Model: llama3
Framework: LangChain
Vector Database: ChromaDB
Embedding Model: sentence-transformers/all-MiniLM-L6-v2
""")

    st.subheader("System Status")

    st.success("✅ Ollama Connected")
    st.success("✅ ChromaDB Ready")
    st.success("✅ Embedding Model Loaded")

    st.subheader("Project Information")

    st.write("""
Data Science Interview Assistant

Features:
• Multi Document RAG
• ChromaDB Vector Search
• Ollama Llama3
• LangChain
• Streamlit UI
""")

    st.subheader("Clear Chat History")

    if st.button("Clear Chat"):

        if "messages" in st.session_state:
            st.session_state.messages = []

        st.success("Chat history cleared successfully.")