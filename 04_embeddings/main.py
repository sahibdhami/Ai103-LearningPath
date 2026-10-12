
from http import client
import os
import numpy as np

from dotenv import load_dotenv
from azure.identity import (
    AzureCliCredential,
    get_bearer_token_provider,
)
from openai import OpenAI

def main() -> None:
    
    load_dotenv()

    credential = AzureCliCredential()

    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default",
    )

    client = OpenAI(
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=token_provider,
    )

    deployment = os.environ["AZURE_EMBEDDING_DEPLOYMENT"]


    def get_embedding(text: str) -> np.ndarray:
        response = client.embeddings.create(
            model=deployment,
            input=text,
        )

        return np.array(
            response.data[0].embedding,
            dtype=np.float32,
        )


    def cosine_similarity(
        vector_a: np.ndarray,
        vector_b: np.ndarray,
    ) -> float:

        dot_product = np.dot(vector_a, vector_b)

        magnitude_a = np.linalg.norm(vector_a)
        magnitude_b = np.linalg.norm(vector_b)

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return float(
            dot_product / (magnitude_a * magnitude_b)
        )

    documents = [
    "Azure Managed Identity enables keyless authentication.",
    "Applications can authenticate without storing credentials.",
    "The weather is sunny today.",
    "Azure Kubernetes Service runs containerized applications.",
    "A good food and water supply is essential for life.",
    "Climate change impacts global ecosystems.",
    "There are many cuisines around the world.",
    "Azure security is crucial for protecting cloud resources.",
    "Noodles are a staple food in many cultures."
    ]

    #query = "How can an application access Azure without secrets?"
    query = input("Enter your query: ")
    query_vector = get_embedding(query)

    results = []

    for document in documents:
        document_vector = get_embedding(document)

        similarity = cosine_similarity(
            query_vector,
            document_vector,
        )

        results.append((document, similarity))

    results.sort(key=lambda item: item[1], reverse=True)

    print("\nTop matching documents:")

    for document, score in results[:9]:
        print(f"{score:.4f} | {document}")

if __name__ == "__main__":
    main()