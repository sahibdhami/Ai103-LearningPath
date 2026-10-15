
import json
import logging
from ai_client import AIResult

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

logger = logging.getLogger("ai-service")


def log_ai_request(result:AIResult)-> None:
    event = {
        "event": "ai_inference_completed",
        "request_id": result.request_id,
        "latency_ms": round(
            result.latency_ms, 2
        ),
        "input_tokens": result.input_tokens,
        "output_tokens": result.output_tokens,
        "success": True,
    }

    logger.info(json.dumps(event))
