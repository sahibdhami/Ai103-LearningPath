
from ai_client import ask_model


TEST_CASES = [
    {
        "question": (
            "What happens when a Kubernetes "
            "readiness probe fails?"
        ),
        "required_concepts": [
            "not ready",
            "traffic",
        ],
    },
    {
        "question": (
            "What is the difference between "
            "authentication and authorization?"
        ),
        "required_concepts": [
            "identity",
            "permission",
        ],
    },
]


def evaluate_answer(answer, required_concepts):
    answer_lower = answer.lower()

    matched = sum(
        1
        for concept in required_concepts
        if concept in answer_lower
    )

    return matched / len(required_concepts)


for test in TEST_CASES:
    result = ask_model(test["question"])

    score = evaluate_answer(
        result.answer,
        test["required_concepts"],
    )

    print("Question:", test["question"])
    print("Answer:", result.answer)
    print("Keyword coverage:", score)
    print("-" * 50)
