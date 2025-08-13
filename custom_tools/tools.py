from database.vector_store import VectorDB

vector_db = VectorDB()
collection = vector_db.get_collection()


def jd_search(
    resume_data: str,
    top_k: int = 3
    ):
    """
    Searches the vector store for documents relevant to a given query.
    Args:
        resume_data (str): Resume text to search for relevant job descriptions.
        top_k (int): The number of top results to return.
    """
    try:

        results = collection.query(
            query_texts=resume_data,
            n_results=top_k,
        )
        return {
            "job_descriptions" : results['documents'][0]
        }
    except Exception as e:
        return f"Error occurred while searching: {str(e)}"
    

def add_document_to_vectorstore(
    job_description: str,
    id: str 
):
    """
    Adds a document to the vector store by reading its content from a specified file path.
    """
    try:

        collection.add(
            documents=job_description,
            metadatas={"source": "job_description"},
            ids=str(id)
        )

        return "Job Description added to vector store successfully."
    except Exception as e:
        return "Error occurred while adding document: " + str(e)