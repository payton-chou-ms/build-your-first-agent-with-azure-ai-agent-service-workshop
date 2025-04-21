import asyncio
import logging
import os
import random
import string

from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import (
    Agent,
    AgentThread,
    AsyncToolSet,
    FileSearchTool,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

from stream_event_handler import StreamEventHandler
from terminal_colors import TerminalColors as tc
from utilities import Utilities

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

load_dotenv()
# Generate a random five-character alphanumeric string
random_suffix = "".join(random.choices(string.ascii_letters + string.digits, k=5))

# Append the random suffix to the agent name
AGENT_NAME = f"Project Spec Agent {random_suffix}"
PROJECT_DATA_SHEET_FILE = "project-requirement.md"
API_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")
PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
if not PROJECT_CONNECTION_STRING:
    raise ValueError("The environment variable 'PROJECT_CONNECTION_STRING' is not set.")

MAX_COMPLETION_TOKENS = 10240
MAX_PROMPT_TOKENS = 20480
# The LLM is used to generate the SQL queries.
# Set the temperature and top_p low to get more deterministic results.
TEMPERATURE = 0.1
TOP_P = 0.1
INSTRUCTIONS_FILE = None


toolset = AsyncToolSet()
utilities = Utilities()


project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=PROJECT_CONNECTION_STRING,
)

INSTRUCTIONS_FILE = "instructions_file_search_for_code.txt"


async def add_agent_tools() -> None:
    """Add tools for the agent."""

    # Add the project requirement data sheet to a new vector data store
    vector_store_project = await utilities.create_vector_store(
        project_client,
        files=[PROJECT_DATA_SHEET_FILE],
        vector_store_name="Project Information Vector Store",
    )
    file_search_project_tool = FileSearchTool(vector_store_ids=[vector_store_project.id])
    toolset.add(file_search_project_tool)


async def initialize() -> tuple[Agent, AgentThread]:
    """Initialize the agent with the sales data schema and instructions."""

    if not INSTRUCTIONS_FILE:
        return None, None

    try:
        instructions = utilities.load_instructions(INSTRUCTIONS_FILE)

        print("Creating agent...")
        agent = await project_client.agents.create_agent(
            model=API_DEPLOYMENT_NAME,
            name=AGENT_NAME,
            instructions=instructions,
            toolset=toolset,
            temperature=TEMPERATURE,
            headers={"x-ms-enable-preview": "true"},
        )
        print(f"Created agent, ID: {agent.id}")
        # Please update the agent ID into the .env file
        print(f"!!! Please update the agent ID into the .env file: {agent.id} !!!")

        print("Creating thread...")
        thread = await project_client.agents.create_thread()
        print(f"Created thread, ID: {thread.id}")

        return agent, thread

    except Exception as e:
        logger.error("An error occurred initializing the agent: %s", str(e))
        logger.error("Please ensure you've enabled an instructions file.")


async def cleanup(agent: Agent, thread: AgentThread) -> None:
    """Cleanup the resources."""
    await project_client.agents.delete_thread(thread.id)
    await project_client.agents.delete_agent(agent.id)


async def post_message(thread_id: str, content: str, agent: Agent, thread: AgentThread) -> None:
    """Post a message to the Azure AI Agent Service."""
    try:
        await project_client.agents.create_message(
            thread_id=thread_id,
            role="user",
            content=content,
        )

        stream = await project_client.agents.create_stream(
            thread_id=thread.id,
            agent_id=agent.id,
            event_handler=StreamEventHandler(project_client=project_client, utilities=utilities, functions=None),
            max_completion_tokens=MAX_COMPLETION_TOKENS,
            max_prompt_tokens=MAX_PROMPT_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            instructions=agent.instructions,
        )
        async with stream as s:
            await s.until_done()
    except Exception as e:
        utilities.log_msg_purple(f"An error occurred posting the message: {e!s}")


async def main() -> None:
    """
    Example questions: Sales by region, top-selling products, total shipping costs by region, show as a pie chart.
    """
    try:
        agent, thread = await initialize()
        if not agent or not thread:
            print(
                f"{tc.BG_BRIGHT_RED}Initialization failed. Ensure you have uncommented the instructions file for the lab.{tc.RESET}"
            )
            print("Exiting...")
            return

        cmd = None
        while True:
            prompt = input(f"\n\n{tc.GREEN}Enter your query (type exit or save to finish): {tc.RESET}").strip()
            if not prompt:
                continue

            cmd = prompt.lower()
            if cmd in {"exit", "save"}:
                break

            await post_message(agent=agent, thread_id=thread.id, content=prompt, thread=thread)

        if cmd == "save":
            print("The agent has not been deleted, so you can continue experimenting with it in the Azure AI Foundry.")
            print(
                f"Navigate to https://ai.azure.com, select your project, then playgrounds, agents playgound, then select agent id: {agent.id}"
            )
        else:
            await cleanup(agent, thread)
            print("The agent resources have been cleaned up.")
    finally:
        # 關閉底層 aiohttp session
        await project_client.close()


if __name__ == "__main__":
    print("Starting async program...")
    asyncio.run(main())
    print("Program finished.")
