
from search import retrieve


test_cases = [
    {
        "question": (
            "How can applications authenticate "
            "without storing credentials?"
        ),
        "relevant_document_ids": [
            "07542b9a5543d21e652c8af0"
        ],
    }
]


def recall_at_k(
    retrieved_ids: set[str],
    relevant_ids: set[str],
) -> float:
    if not relevant_ids:
        return 0.0

    return len(
        retrieved_ids & relevant_ids
    ) / len(relevant_ids)


def evaluate():
    for test in test_cases:
        results = retrieve(
            test["question"],
            top_k=5,
        )

        retrieved_ids = {
            r["document_id"] for r in results
        }

        relevant_ids = set(
            test["relevant_document_ids"]
        )

        score = recall_at_k(
            retrieved_ids,
            relevant_ids,
        )

        print("Question:", test["question"])
        print(f"Recall@5: {score:.2%}")


if __name__ == "__main__":
    evaluate()
