import os
import json
from xmlrpc import client
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import (AzureCliCredential, get_bearer_token_provider)

def main() -> None:
    load_dotenv()
    azureOpenAIEndpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    modelDeployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    scope = "https://cognitiveservices.azure.com/.default"

    credential = AzureCliCredential()
    token_provider = get_bearer_token_provider(
        credential,
        scope,
        )

    client = OpenAI(base_url=azureOpenAIEndpoint,
                    api_key=token_provider,
    )

    response = client.responses.create(
        model=modelDeployment,
        instructions="You are an Azure AI certification instructor. "
        "Explain concepts clearly and compare with GCP "
        "and C#/.NET when useful.",
        input="What is Azure Managed Identity?",
        temperature=0.2,
        max_output_tokens=200,
    )

    print(response.output)

if __name__ == "__main__":
    main()