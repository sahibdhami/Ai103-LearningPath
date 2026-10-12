import os
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import (AzureCliCredential, get_bearer_token_provider)
from models import SupportTicket

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

    customer_message = (
        "I was charged twice for my subscription. "
        "Please refund the extra payment immediately."
    )

    response = client.responses.parse(
        model=modelDeployment,
        instructions=(
            "Classify the customer support request. "
            "Return accurate structured data. "
            "Flag requests requiring account actions "
            "or financial adjustments for human review."
        ),       
        input=customer_message,
        temperature=0.2,
        max_output_tokens=200,
        text_format=SupportTicket,
    )

    parsed_reponse = response.output_parsed

    if parsed_reponse is None:
        raise RuntimeError(
            "No parsed ticket returned. "
            "Inspect the response for refusal or incomplete output."
        )
    
    print("\nStructured Ticket:")
    responseInJson = parsed_reponse.model_dump_json(indent=2)
    print(responseInJson)
    print("\nPython Object Properties:")
    print("Category:", parsed_reponse.category)
    print("Priority:", parsed_reponse.priority)
    print("Human review:", parsed_reponse.requires_human_review)
    print("Customer sentiment:", parsed_reponse.customer_sentiment)
    print("Suggested action:", parsed_reponse.suggested_action)

    route = route_ticket(parsed_reponse)
    print("Route:", route)
    
def route_ticket(ticket: SupportTicket) -> str:
    if ticket.requires_human_review:
        return "human-review-queue"

    if ticket.category == "Billing":
        return "billing-queue"

    if ticket.category == "Technical":
        return "technical-support-queue"

    if ticket.customer_sentiment == "Negative":
        return "escalation-queue"
    
    if ticket.suggested_action.lower().startswith("refund"):
        return "billing-queue"
    
    return "general-support-queue"

if __name__ == "__main__":
    main()