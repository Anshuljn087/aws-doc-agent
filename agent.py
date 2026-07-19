import json
import os
import re
import time
from pathlib import Path
from typing import List, Dict, Any


DOCS_DIR = Path(__file__).resolve().parent / "docs"

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
KB_ID = os.getenv("KB_ID")
MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-sonnet-4-5-20250929-v1:0")

bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)
bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name=AWS_REGION)

CACHE_TTL_SECONDS = 10 * 60
_answer_cache: Dict[str, Dict[str, Any]] = {}
_cache_hits = 0


def _normalize_query(query: str) -> str:
    return " ".join(query.strip().lower().split())


def _get_cached_answer(query: str) -> str | None:
    normalized_query = _normalize_query(query)
    cached_entry = _answer_cache.get(normalized_query)
    if not cached_entry:
        return None

    if time.time() - cached_entry["timestamp"] > CACHE_TTL_SECONDS:
        _answer_cache.pop(normalized_query, None)
        return None

    global _cache_hits
    _cache_hits += 1
    print(f"[cache] hit for: {normalized_query}")
    return cached_entry["answer"]


def _store_cached_answer(query: str, answer: str) -> None:
    normalized_query = _normalize_query(query)
    _answer_cache[normalized_query] = {
        "answer": answer,
        "timestamp": time.time(),
    }


def get_cache_stats() -> Dict[str, int]:
    return {"cached_queries": len(_answer_cache), "cache_hits": _cache_hits}


def _load_local_docs() -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for path in DOCS_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        results.append({"content": {"text": text}, "source": str(path.name)})
    return results


_STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "was", "were", "be", "been",
    "what", "how", "does", "do", "did", "with", "and", "or", "to", "of",
    "in", "on", "for", "it", "this", "that", "i", "you", "we", "can",
}


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 1 and token not in _STOPWORDS}


def _rank_local_docs(query: str, docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    query_tokens = _tokenize(query)
    ranked: List[Dict[str, Any]] = []
    for doc in docs:
        text = doc.get("content", {}).get("text", "")
        doc_tokens = _tokenize(text)
        score = len(query_tokens & doc_tokens)
        if score > 0:
            ranked.append({**doc, "_score": score})
    ranked.sort(key=lambda item: item["_score"], reverse=True)
    return ranked


def _answer_from_local_docs(query: str, docs: List[Dict[str, Any]]) -> str:
    query_lower = query.lower()
    for doc in docs:
        text = doc.get("content", {}).get("text", "")
        if "enable versioning" in query_lower and "to enable versioning" in text.lower():
            return text.split("To enable versioning", 1)[1].split("\n\n", 1)[0].strip()
        if "enable" in query_lower and "to enable" in text.lower():
            return text.split("To enable", 1)[1].split("\n\n", 1)[0].strip()
        if any(token in text.lower() for token in ["versioning", "lambda", "iam", "vpc", "dynamodb", "cloudwatch", "bedrock"]):
            paragraphs = [part.strip() for part in text.split("\n\n") if part.strip() and not part.strip().startswith("#")]
            if paragraphs:
                return paragraphs[0]
    return "I could not find a suitable local documentation answer for that question."


def retrieve(query: str) -> List[Dict[str, Any]]:
    if not KB_ID:
        docs = _load_local_docs()
        return _rank_local_docs(query, docs)

    candidate_configs = [
        {"managedSearchConfiguration": {"numberOfResults": 5}},
        {"vectorSearchConfiguration": {"numberOfResults": 5}},
    ]

    last_error: Exception | None = None
    for retrieval_config in candidate_configs:
        try:
            response = bedrock_agent_runtime.retrieve(
                knowledgeBaseId=KB_ID,
                retrievalQuery={"text": query},
                retrievalConfiguration=retrieval_config,
            )
            return response.get("retrievalResults", [])
        except ClientError as exc:
            last_error = exc
            if "Incompatible configuration" not in str(exc) and "Unknown parameter" not in str(exc):
                raise

    if last_error is not None:
        raise last_error

    return []


def _reformulate_query(query: str, history: List[Dict[str, Any]] | None) -> str:
    if not history:
        return query

    recent_history = history[-3:]
    history_text = "\n".join(f"{item.get('role', 'user')}: {item.get('content', '')}" for item in recent_history)
    prompt = (
        "Given this conversation history, rewrite the follow-up message as a standalone question. "
        "Return only the rewritten question.\n\n"
        f"History:\n{history_text}\n\n"
        f"Follow-up: {query}"
    )

    try:
        response = bedrock_runtime.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 120,
                "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
                "temperature": 0.1,
            }),
        )
        response_body = json.loads(response.get("body").read())
        rewritten = response_body["content"][0]["text"].strip()
        return rewritten or query
    except Exception:
        return query


def generate(query: str, chunks: List[Dict[str, Any]], history: List[Dict[str, Any]] | None = None) -> str:
    context_text = "\n\n".join(
        chunk.get("content", {}).get("text", "")
        for chunk in chunks
        if chunk.get("content", {}).get("text")
    )

    recent_history = (history or [])[-2:]
    history_text = ""
    if recent_history:
        history_text = "\n\nConversation history:\n" + "\n".join(
            f"{item.get('role', 'user')}: {item.get('content', '')}" for item in recent_history
        )

    prompt = (
        "You are a concise AWS documentation assistant. "
        "Answer the user's question using only the supplied context. "
        "If the answer is not present in the context, say you do not have enough information.\n\n"
        f"User question: {query}{history_text}\n\n"
        f"Context:\n{context_text}"
    )

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        "temperature": 0.2,
    }

    try:
        response = bedrock_runtime.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
        )
    except ClientError as exc:
        return f"I could not generate an answer because the Bedrock model call failed: {exc}"

    try:
        response_body = json.loads(response.get("body").read())
        return response_body["content"][0]["text"]
    except (KeyError, json.JSONDecodeError, AttributeError) as exc:
        return f"I could not parse the Bedrock response: {exc}"


def agent_answer(query: str, history: List[Dict[str, Any]] | None = None) -> str:
    standalone_query = _reformulate_query(query, history)
    cached_answer = _get_cached_answer(standalone_query)
    if cached_answer is not None:
        return cached_answer

    try:
        chunks = retrieve(standalone_query)
    except Exception as exc:
        local_docs = _rank_local_docs(standalone_query, _load_local_docs())
        return _answer_from_local_docs(standalone_query, local_docs) if local_docs else f"I could not retrieve documentation from the Knowledge Base right now. Please verify your AWS credentials and Bedrock configuration. ({exc})"

    if not chunks:
        local_docs = _rank_local_docs(standalone_query, _load_local_docs())
        if local_docs:
            return _answer_from_local_docs(standalone_query, local_docs)
        return "No relevant AWS documentation was found for that question. Please try a different phrasing or confirm the knowledge base contains the topic."

    if len(chunks) < 2:
        refined_query = f"Explain {standalone_query} in AWS documentation terms with clear examples"
        try:
            refined_chunks = retrieve(refined_query)
        except Exception:
            refined_chunks = []
        if refined_chunks:
            chunks = refined_chunks

    if not chunks:
        local_docs = _rank_local_docs(standalone_query, _load_local_docs())
        if local_docs:
            return _answer_from_local_docs(standalone_query, local_docs)
        return "No relevant AWS documentation was found for that question. Please try a different phrasing or confirm the knowledge base contains the topic."

    answer = generate(standalone_query, chunks, history)
    if "do not have enough information" in answer.lower() or "could not" in answer.lower() or "failed" in answer.lower():
        local_docs = _rank_local_docs(standalone_query, _load_local_docs())
        if local_docs:
            answer = _answer_from_local_docs(standalone_query, local_docs)
    _store_cached_answer(standalone_query, answer)
    return answer
