
import os

from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=AzureCliCredential(),
)

agent = project.agents.create_version(
    agent_name=os.environ["FOUNDRY_AGENT_NAME"],
    definition=PromptAgentDefinition(
        model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
        instructions=(
            "You are a cloud engineering assistant. "
            "Explain operational concepts clearly. "
            "Do not claim to have checked live systems "
            "unless a connected tool provides evidence."
        ),
    ),
)

print("Agent name:", agent.name)
print("Agent version:", agent.version)
    