
import os
import time
import uuid

from dataclasses import dataclass

from azure.identity import (
    DefaultAzureCredential,
    get_bearer_token_provider,
)
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

credential = DefaultAzureCredential()

token_provider = get_bearer_token_provider(
    credential,
    "https://cognitiveservices.azure.com/.default",
)

client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=token_provider,
    timeout=30.0,
    max_retries=2,
)

deployment = os.environ["AZURE_CHAT_DEPLOYMENT"]


@dataclass
class AIResult:
    request_id: str
    answer: str
    latency_ms: float
    input_tokens: int
    output_tokens: int


def ask_model(question: str) -> AIResult:
    if not question or not question.strip():
        raise ValueError("Question is required")

    if len(question) > 4000:
        raise ValueError("Question is too long")

    request_id = str(uuid.uuid4())
    start = time.perf_counter()

    response = client.responses.create(
        model=deployment,
        instructions=(
            "You are a logistics support assistant. "
            "Provide concise, accurate explanations. "
            "Do not invent operational facts. "
            "If a live system has not been queried, "
            "say that live status is unverified."
        ),
        input=question,
        max_output_tokens=500,
    )

    latency_ms = (
        time.perf_counter() - start
    ) * 1000

    usage = response.usage

    return AIResult(
        request_id=request_id,
        answer=response.output_text,
        latency_ms=latency_ms,
        input_tokens=(
            usage.input_tokens if usage else 0
        ),
        output_tokens=(
            usage.output_tokens if usage else 0
        ),
    )
