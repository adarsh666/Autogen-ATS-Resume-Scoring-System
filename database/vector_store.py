import chromadb
from  chromadb.utils import embedding_functions


class VectorDB:
    def __init__(self):

        chroma_client = chromadb.PersistentClient(path='./vector_store')
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        collections = chroma_client.list_collections()
        if len(collections) == 0:
            self.collection = chroma_client.create_collection(
            name = "resume_collection",
            embedding_function=sentence_transformer_ef)
        else:
            self.collection = chroma_client.get_collection(name = "resume_collection")

    def get_collection(self):
        return self.collection