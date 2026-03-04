from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from qdrant_client import QdrantClient

from app.config import settings


def get_vector_store():
    client = QdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
    )

    vector_store = QdrantVectorStore(
        client=client,
        collection_name=settings.collection_name,
    )

    return vector_store


def get_index():
    vector_store = get_vector_store()

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    print("API KEY:", settings.openai_api_key)

    # Configurar embeddings
    embed_model = OpenAIEmbedding(
        api_key=settings.openai_api_key
    )

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
        embed_model=embed_model,
    )

    return index