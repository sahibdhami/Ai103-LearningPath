
from ai_client import ask_model
from monitoring import log_ai_request

def main():
    question = (
        "Explain how Kubernetes readiness probes "
        "differ from liveness probes."
    )

    result = ask_model(question)

    print("\nAI Answer:\n")
    print(result.answer)

    log_ai_request(result)


if __name__ == "__main__":
    main()
