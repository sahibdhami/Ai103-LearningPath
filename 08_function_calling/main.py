from agent import ask_agent

def main():
    print("AI Tool-Calling Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        try:
            answer = ask_agent(question)
            print(f"\nAssistant: {answer}\n")

        except Exception as exc:
            print(
                f"\nRequest failed: "
                f"{type(exc).__name__}: {exc}\n"
            )


if __name__ == "__main__":
    main()
