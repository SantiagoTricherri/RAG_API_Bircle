from typing import List

from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.openai import OpenAI

from app.services.vector_store import get_index
from app.config import settings


def query_rag(question: str, top_k: int = 5):
    index = get_index()

    retriever = index.as_retriever(similarity_top_k=top_k)

    llm = OpenAI(api_key=settings.openai_api_key)

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=llm,
        system_prompt=(
            "You are a helpful assistant. "
            "Answer ONLY using the provided context. "
            "If the answer is not in the context, say that you don't have enough information."
        ),
    )

    response = query_engine.query(question)

    MIN_SCORE = 0.8

    sources = []
    for node in response.source_nodes:
        if node.score and node.score >= MIN_SCORE:
            sources.append(
                {
                    "doc_id": node.node.node_id,
                    "filename": node.node.metadata.get("filename"),
                    "score": node.score,
                    "snippet": node.node.text.strip().replace("\n", " ")[:200],
                }
            )

    if not sources:
        return {
            "answer": "No relevant context found to answer the question.",
            "sources": [],
            "retrieval_params": {"top_k": top_k},
        }

    return {
        "answer": str(response),
        "sources": sources,
        "retrieval_params": {"top_k": top_k},
    }