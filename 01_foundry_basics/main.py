
import os
import json
import base64

from dotenv import load_dotenv
from azure.identity import (
    AzureCliCredential,
    get_bearer_token_provider,
)
from openai import OpenAI, AuthenticationError


def main():
    load_dotenv()

    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]

    print("Endpoint:", endpoint)
    print("Deployment:", deployment)

    # Force the same identity used by az login
    credential = AzureCliCredential()

    scope = "https://cognitiveservices.azure.com/.default"

    # Verify we can obtain a token
    token = credential.get_token(scope).token
    print("Token acquired:", bool(token))

    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)

    claims = json.loads(base64.urlsafe_b64decode(payload))

    print("Audience:", claims.get("aud"))
    print("Tenant:", claims.get("tid"))
    print("Principal:", claims.get("oid"))


    token_provider = get_bearer_token_provider(
        credential,
        scope,
    )

    client = OpenAI(
        base_url=endpoint,
        api_key=token_provider,
    )

    try:
        response = client.responses.create(
            model=deployment,
            input="Azure Managed Identity vs GCP Workload Identity Federation",
        )

        print("Response:", response.model_dump_json(indent=2))

    except AuthenticationError as error:
        print("Authentication failed")
        print("Status:", error.status_code)
        print("Details:", error.message)


if __name__ == "__main__":
    main()
