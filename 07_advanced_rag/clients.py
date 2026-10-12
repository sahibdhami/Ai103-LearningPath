
import os

from dotenv import load_dotenv
from azure.identity import AzureCliCredential, get_bearer_token_provider
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from openai import OpenAI

load_dotenv()

credential = AzureCliCredential()

token_provider = get_bearer_token_provider(
    credential,
    "https://cognitiveservices.azure.com/.default",
)

openai_client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=token_provider,
)

search_endpoint = os.environ["AZURE_SEARCH_ENDPOINT"]
index_name = os.environ["AZURE_ADV_SEARCH_INDEX"]

index_client = SearchIndexClient(
    endpoint=search_endpoint,
    credential=credential,
)

search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=credential,
)


def embed(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        model=os.environ["AZURE_EMBEDDING_DEPLOYMENT"],
        input=text,
    )
    return response.data[0].embedding
