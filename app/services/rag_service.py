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
        "If the context does not explicitly mention the exact person "
        "or entity asked in the question, say you don't have enough information."
    ),
    )

    response = query_engine.query(question)

    MIN_SCORE = 0.6
    STRICT_SCORE = 0.7

    valid_nodes = [
        node for node in response.source_nodes
        if node.score and node.score >= MIN_SCORE
    ]

    if not valid_nodes:
        return {
            "answer": "No relevant context found to answer the question.",
            "sources": [],
            "retrieval_params": {"top_k": top_k},
        }

    best_score = max(node.score for node in valid_nodes)

    if best_score < STRICT_SCORE:
        return {
            "answer": "No relevant context found to answer the question.",
            "sources": [],
            "retrieval_params": {"top_k": top_k},
        }

    sources = [
        {
            "doc_id": node.node.node_id,
            "filename": node.node.metadata.get("filename"),
            "score": node.score,
            "snippet": node.node.text.strip().replace("\n", " ")[:200],
        }
        for node in valid_nodes
    ]

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