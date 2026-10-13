
from agent import InvestigationAgent


def main():
    agent = InvestigationAgent()

    print("Logistics Investigation Agent")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        try:
            answer = agent.ask(question)

            print("\nAgent:")
            print(answer)

            print(
                "\nTotal tool calls:",
                agent.state.tool_calls,
            )
            print()

        except Exception as exc:
            print(
                f"Agent error: "
                f"{type(exc).__name__}: {exc}"
            )


if __name__ == "__main__":
    main()
