import base64
import mimetypes
import os
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import (
    AzureCliCredential,
    get_bearer_token_provider,
)
from openai import OpenAI

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


def analyze_image(
    image_path: str,
    question: str,
) -> str:
    path = Path(image_path)

    mime_type, _ = mimetypes.guess_type(path.name)

    if mime_type not in (
        "image/jpeg",
        "image/png",
        "image/webp",
    ):
        raise ValueError("Unsupported image format")

    image_bytes = path.read_bytes()

    encoded = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    image_url = (
        f"data:{mime_type};base64,{encoded}"
    )

    response = client.responses.create(
        model=os.environ["AZURE_VISION_DEPLOYMENT"],
        instructions=(
            "You inspect package photographs. "
            "Describe only what is visually observable. "
            "Identify possible visible damage. "
            "Do not invent package IDs, tracking events, "
            "or internal contents. "
            "State uncertainty when the image is unclear."
        ),
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": question,
                    },
                    {
                        "type": "input_image",
                        "image_url": image_url,
                    },
                ],
            }
        ],
    )

    return response.output_text


if __name__ == "__main__":
    result = analyze_image(
        "samples/package.jpeg",
        (
            "Describe the package condition. "
            "Is there visible evidence of damage?"
        ),
    )

    print(result)
