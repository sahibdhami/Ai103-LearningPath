
import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import (
    DocumentIntelligenceClient,
)

load_dotenv()

client = DocumentIntelligenceClient(
    endpoint=os.environ["AZURE_DOCUMENT_ENDPOINT"],
    credential=AzureKeyCredential(
        os.environ["AZURE_DOCUMENT_KEY"]
    ),
)


def analyze_invoice(path: str):
    with open(path, "rb") as document:
        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice",
            body=document,
            content_type="application/octet-stream",
        )

        result = poller.result()

    for invoice in result.documents or []:
        print("\nDocument type:", invoice.doc_type)

        for field_name, field in invoice.fields.items():
            value = (
                field.content
                if field.content is not None
                else str(field.value)
            )

            print(
                field_name,
                ":",
                value,
                "| Confidence:",
                field.confidence,
            )


if __name__ == "__main__":
    analyze_invoice("samples/invoice.pdf")
