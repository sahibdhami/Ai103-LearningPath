
import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

load_dotenv()

client = TextAnalyticsClient(
    endpoint=os.environ["AZURE_LANGUAGE_ENDPOINT"],
    credential=AzureKeyCredential(
        os.environ["AZURE_LANGUAGE_KEY"]
    ),
)

message = (
    "My package UPS12345 was supposed to arrive "
    "in Atlanta on October 10. It is still delayed, "
    "and I'm very disappointed."
)

# Sentiment
sentiment = client.analyze_sentiment(
    [message]
)[0]

print("Sentiment:", sentiment.sentiment)
print("Confidence:", sentiment.confidence_scores)

# Named entities
entities = client.recognize_entities(
    [message]
)[0]

for entity in entities.entities:
    print(
        "Entity:",
        entity.text,
        "| Category:",
        entity.category,
        "| Confidence:",
        entity.confidence_score,
    )

# Key phrases
phrases = client.extract_key_phrases(
    [message]
)[0]

print("Key phrases:", phrases.key_phrases)
