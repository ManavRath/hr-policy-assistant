from llm import llm
from sentence_transformers import SentenceTransformer
import chromadb
from documents import documents

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB (EphemeralClient replaces deprecated Client())
client = chromadb.EphemeralClient()
collection = client.create_collection(name="hr_policy")

# Add documents to the collection
texts = [doc["text"] for doc in documents]
ids = [doc["id"] for doc in documents]
metadatas = [{"topic": doc["topic"]} for doc in documents]

embeddings = model.encode(texts).tolist()

collection.add(
    documents=texts,
    embeddings=embeddings,
    ids=ids,
    metadatas=metadatas
)


def retrieve(query: str, n_results: int = 3):
    """Retrieve top-n relevant document chunks for a query."""
    # Guard: clamp n_results to collection size
    n_results = min(n_results, collection.count())
    if n_results == 0:
        return "", []

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    retrieved_docs = results["documents"][0]
    sources = results["metadatas"][0]

    context = ""
    for i, doc in enumerate(retrieved_docs):
        context += f"[{sources[i]['topic']}] {doc}\n"

    return context, sources


def generate_answer(query: str, chat_history: list = None) -> str:
    """
    Generate an answer using RAG + LLM.

    Args:
        query: The user's question.
        chat_history: A list of strings representing previous turns.
                      Managed externally (e.g., Streamlit session_state)
                      to avoid cross-user/session contamination.

    Returns:
        The LLM's answer string.
    """
    if not query or not query.strip():
        return "Please enter a valid question."

    if chat_history is None:
        chat_history = []

    context, _ = retrieve(query)

    history_str = "\n".join(chat_history) if chat_history else "None"

    prompt = f"""You are an HR assistant.

Conversation so far:
{history_str}

Answer ONLY using the context below.
If the answer is not found in the context, say "I don't know based on the available HR policy.".

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    context, sources = retrieve("leave policy")
    print(context)