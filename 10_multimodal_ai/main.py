
from speech import transcribe_audio

# Import the InvestigationAgent from Lesson 10.
# Copy that project's agent.py and dependencies
# into this project or package them as a module.
from agent import InvestigationAgent


def main():
    transcript = transcribe_audio(
        "samples/customer-call.wav"
    )

    print("Customer said:")
    print(transcript)

    agent = InvestigationAgent()

    answer = agent.ask(transcript)

    print("\nAI Assistant:")
    print(answer)


if __name__ == "__main__":
    main()
