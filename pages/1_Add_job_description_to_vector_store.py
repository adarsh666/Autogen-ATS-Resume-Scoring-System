import uuid
import streamlit as st
import chromadb
from chromadb.config import Settings

# Initialize Chroma client (local persistence)
client = chromadb.PersistentClient(path="./vector_store")

# Create / get a collection
collection_name = "my_collection"
collection = client.get_or_create_collection(name=collection_name)

st.title("📦 ChromaDB Manager")

# Section 1: Add data to ChromaDB
st.subheader("Add Data to ChromaDB")
text_data = st.text_area("Document Text", placeholder="Enter your text here")
# metadata_input = st.text_input("Metadata (key=value)", placeholder="type=note")

if st.button("Add to ChromaDB"):
    if text_data.strip():
        # Generate a unique ID
        doc_id = str(uuid.uuid4())

        # Parse metadata
        metadata = {"type" : "job_description"}

        # Add to collection
        collection.add(
            ids=[doc_id],
            documents=[text_data],
            metadatas=[metadata] if metadata else None
        )
        st.success(f"✅ Added document with ID: {doc_id}")
    else:
        st.error("❌ Please provide both an ID and text.")

# Section 2: Display all items in ChromaDB
st.subheader("Stored Items in ChromaDB")
items = collection.peek(limit=50)  # Get first 50 entries

if items and "ids" in items and items["ids"]:
    for idx, doc_id in enumerate(items["ids"]):
        st.markdown(f"**ID:** {doc_id}")
        st.markdown(f"**Text:** {items['documents'][idx]}")
        if items["metadatas"] and items["metadatas"][idx]:
            st.markdown(f"**Metadata:** {items['metadatas'][idx]}")
        st.markdown("---")
else:
    st.info("📭 No items found in the collection.")

# ------------------------
# Section 3: Delete by ID
# ------------------------
st.subheader("Delete Document by ID")
delete_id = st.text_input("Enter Document ID to Delete")

if st.button("Delete Document"):
    if delete_id.strip():
        try:
            collection.delete(ids=[delete_id.strip()])
            st.success(f"🗑️ Document with ID `{delete_id}` deleted successfully.")
        except Exception as e:
            st.error(f"❌ Error deleting document: {str(e)}")
    else:
        st.error("❌ Please enter a valid ID.")
