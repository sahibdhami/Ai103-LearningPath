
import os
from pathlib import Path

from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures

load_dotenv()

client = ImageAnalysisClient(
    endpoint=os.environ["AZURE_VISION_ENDPOINT"],
    credential=AzureCliCredential(),
)


def extract_text(image_path: str) -> list[str]:
    image_bytes = Path(image_path).read_bytes()

    result = client.analyze(
        image_data=image_bytes,
        visual_features=[VisualFeatures.READ],
    )

    lines = []

    if result.read:
        for block in result.read.blocks:
            for line in block.lines:
                lines.append(line.text)

    return lines


if __name__ == "__main__":
    lines = extract_text(
        "samples/shipping-label.png"
    )

    print("Extracted text:")

    for line in lines:
        print(line)
