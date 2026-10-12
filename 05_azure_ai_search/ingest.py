
from common import search_client, embed

documents = [
    {
        "id": "1",
        "title": "Azure Managed Identity",
        "category": "security",
        "content": (
            "Azure Managed Identity allows applications "
            "to authenticate to supported Azure resources "
            "without storing credentials."
        ),
    },
    {
        "id": "2",
        "title": "GKE Workload Identity Federation",
        "category": "security",
        "content": (
            "GKE Workload Identity Federation enables "
            "Kubernetes workloads to access Google Cloud "
            "APIs without service account key files."
        ),
    },
    {
        "id": "3",
        "title": "Kubernetes HPA",
        "category": "kubernetes",
        "content": (
            "Horizontal Pod Autoscaler automatically "
            "adjusts Kubernetes replica counts based "
            "on configured resource or custom metrics."
        ),
    },
    {
        "id": "4",
        "title": "GCP Pub/Sub",
        "category": "messaging",
        "content": (
            "Google Cloud Pub/Sub supports asynchronous "
            "messaging between distributed applications "
            "using topics and subscriptions."
        ),
    },
    {
        "id": "5",
        "title": "Azure AI Search",
        "category": "ai",
        "content": (
            "Azure AI Search supports keyword, vector "
            "and hybrid retrieval for AI applications."
        ),
    },
]


def ingest_documents():
    for document in documents:
        document["content_vector"] = embed(
            document["content"]
        )

    results = search_client.upload_documents(
        documents=documents
    )

    for result in results:
        print(
            f"Document {result.key}: "
            f"{'success' if result.succeeded else 'failed'}"
        )


if __name__ == "__main__":
    ingest_documents()
