import os
import time
from datetime import datetime
from typing import List

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.schema import Document

from app.services.vector_store import get_index


DATA_DIR = "data"


def ingest_directory(directory_path: str = DATA_DIR):
    if not os.path.exists(directory_path):
        raise ValueError("Directory does not exist")

    reader = SimpleDirectoryReader(
        input_dir=directory_path,
        required_exts=[".txt", ".pdf"],
    )

    documents = reader.load_data()

    if not documents:
        return {"ingested": 0, "message": "No documents found"}

    enriched_docs = []
    for doc in documents:
        metadata = doc.metadata or {}

        metadata.update(
            {
                "filename": metadata.get("file_name"),
                "ingest_timestamp": datetime.utcnow().isoformat(),
            }
        )

        enriched_docs.append(
            Document(
                text=doc.text,
                metadata=metadata,
            )
        )

    index = get_index()

    index.insert_nodes(
        SimpleNodeParser().get_nodes_from_documents(enriched_docs)
    )

    return {"ingested": len(enriched_docs)}