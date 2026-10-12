
from rag_service import ask

def main():
    print("Cloud Engineering Knowledge Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Question: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        answer, sources = ask(question)

        print("\nAnswer:")
        print(answer)

        print("\nRetrieved sources:")

        for source in sources:
            print(
                f"[{source['id']}] {source['title']}"
            )

        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()
