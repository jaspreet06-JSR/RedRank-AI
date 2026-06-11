def retrieval_score(candidate):

    HIGH_VALUE = [
        "recommendation",
        "re-ranking",
        "reranking",
        "learning to rank",
        "semantic search",
        "vector",
        "embedding",
        "retrieval",
        "pinecone",
        "weaviate",
        "qdrant",
        "pgvector",
        "opensearch",
        "faiss",
        "milvus",
        "rag"
    ]

    MEDIUM_VALUE = [
        "llm",
        "nlp",
        "transformer",
        "fine-tuning",
        "langchain",
        "llamaindex",
        "sentence transformer"
    ]

    text = ""

    for exp in candidate.get("career_history", []):
        text += " " + exp.get("description", "").lower()

    for skill in candidate.get("skills", []):
        text += " " + skill.get("name", "").lower()

    score = 0

    for keyword in HIGH_VALUE:
        if keyword in text:
            score += 2

    for keyword in MEDIUM_VALUE:
        if keyword in text:
            score += 1

    return min(score / 20, 1.0)