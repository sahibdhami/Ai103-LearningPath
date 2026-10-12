
from azure.search.documents.models import VectorizedQuery

from common import search_client, embed

def search_documents(
    question: str,
    mode: str = "hybrid",
):
    if mode not in ("vector", "lexical", "hybrid"):
        raise ValueError("Invalid search mode")

    vector_queries = []

    if mode in ("vector", "hybrid"):
        query_vector = embed(question)

        vector_queries.append(
            VectorizedQuery(
                vector=query_vector,
                k_nearest_neighbors=5,
                fields="content_vector",
            )
        )

    search_text = (
        question if mode in ("lexical", "hybrid")
        else None
    )

    results = search_client.search(
        search_text=search_text,
        vector_queries=vector_queries,
        select=["id", "title", "content", "category"],
        top=3,
    )

    print(f"\nSearch mode: {mode}")

    for result in results:
        print("-" * 50)
        print("Title:", result["title"])
        print("Category:", result["category"])
        print("Score:", result["@search.score"])
        print("Content:", result["content"])


if __name__ == "__main__":
    question = input("Enter your question: ")

    for mode in ("lexical", "vector", "hybrid"):
        search_documents(question, mode)
