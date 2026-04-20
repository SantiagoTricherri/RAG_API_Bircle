from typing import List

from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.llms.openai import OpenAI

from app.services.vector_store import get_index
from app.config import settings


def query_rag(question: str, top_k: int = 8):
    index = get_index()

    retriever = index.as_retriever(similarity_top_k=top_k)

    llm = OpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key)

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=llm,
        system_prompt=(
            "IMPORTANTE: Respondé SIEMPRE en español, sin excepciones. "
            "Nunca respondas en inglés bajo ninguna circunstancia, "
            "incluso si no encontrás información relevante. "
            "Sos NexusAI, un asistente académico universitario. "
            "REGLA ABSOLUTA: Respondé SIEMPRE en español, sin excepciones, sin importar el idioma de la pregunta. "
            "Nunca respondas en inglés ni en ningún otro idioma que no sea español. "
            "Se te va a proporcionar contexto extraído de documentos académicos. "
            "Si el contexto contiene información relacionada con la pregunta, aunque sea de forma parcial o indirecta, "
            "usala y respondé con lo que tenés disponible, siendo lo más completo posible. "
            "Solo decí que no tenés información suficiente si el contexto está completamente vacío "
            "o no tiene absolutamente ninguna relación con el tema preguntado. "
            "Nunca inventes información que no esté en el contexto. "
            "Respondé como si el usuario no tuviera acceso al contexto que vos tenés — "
            "tu respuesta debe ser autocontenida y comprensible sin contexto adicional. "
            "Nunca uses referencias relativas al contexto como 'al actual', 'el mencionado', "
            "'dicho estudio', 'según lo indicado', 'el mencionado anteriormente', 'el documento actual'. "
            "Siempre nombrá explícitamente el concepto, persona, estudio o documento al que te referís. "
            "Si vas a mencionar un test, estudio o concepto, decí su nombre completo cada vez. "
            "Respondé de forma clara, útil y conversacional, como un asistente académico real. "
            "Recordatorio final: tu respuesta debe estar en español siempre."
        ),
    )

    response = query_engine.query(question)

    MIN_SCORE = 0.3
    STRICT_SCORE = 0.5

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