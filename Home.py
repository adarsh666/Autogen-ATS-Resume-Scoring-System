import streamlit as st

# App title
st.set_page_config(page_title="My Streamlit App", page_icon="🚀")

st.title("🚀 Welcome to My Streamlit App")
st.write("""
This is the main home page of your multipage app.  
Use the **sidebar** to navigate to other pages like:
- 📦 ChromaDB Manager  
- 📄 Document Uploader
""")

st.info("💡 Tip: You can add as many pages as you want inside the `pages/` folder.")
