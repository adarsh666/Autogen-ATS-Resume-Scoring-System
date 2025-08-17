import streamlit as st
import pandas as pd

from custom_tools.mongodb import get_collection

collection = get_collection()

st.set_page_config(page_title="MongoDB Viewer", page_icon="🗄️")
st.title("🗄️ MongoDB Data Viewer")

# Fetch data
def load_data():
    return list(collection.find({}, {"_id": 0}))  # Exclude _id

documents = load_data()

if documents:
    df = pd.DataFrame(documents)  
    st.dataframe(df)

    # Select row to delete
    st.subheader("🗑️ Delete a Document")

    # Let user pick by unique field (e.g., name or email)
    delete_field = st.selectbox("Select field for identifying record:", df.columns)

    unique_values = df[delete_field].unique().tolist()
    value_to_delete = st.selectbox(f"Select {delete_field} to delete:", unique_values)

    if st.button("Delete Record"):
        result = collection.delete_one({delete_field: value_to_delete})
        if result.deleted_count > 0:
            st.success(f"Record with {delete_field}='{value_to_delete}' deleted successfully ✅")
            st.experimental_rerun()
        else:
            st.error("No matching record found ❌")

else:
    st.warning("No data found in the collection.")

# Option to refresh manually
if st.button("🔄 Refresh Data"):
    st.experimental_rerun()
