# Copyright (c) Microsoft. All rights reserved.

import asyncio

from azure.identity.aio import DefaultAzureCredential

from semantic_kernel.agents import AgentGroupChat, AzureAIAgent, AzureAIAgentSettings
from semantic_kernel.agents.strategies import TerminationStrategy
from semantic_kernel.contents import AuthorRole

"""
以下範例展示如何建立一個使用 Azure OpenAI 或 OpenAI 的 OpenAI 助手，
一個聊天完成代理，並讓他們參與群組聊天，
以共同達成使用者的需求。
"""


class ApprovalTerminationStrategy(TerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return "approved" in history[-1].content.lower()


REVIEWER_NAME = "ArtDirector"
REVIEWER_INSTRUCTIONS = """
你是一位藝術總監，對廣告文案有著獨到見解，源於對大衛·奧格威的熱愛。
目標是判斷給定的文案是否適合印刷。
如果適合，請表示該文案已獲批准。除非你正在給予批准，否則請勿使用「批准」這個詞。
如果不適合，請提供有關如何改進建議文案的見解，而不需給出範例。
"""

COPYWRITER_NAME = "CopyWriter"
COPYWRITER_INSTRUCTIONS = """
你是一位擁有十年經驗的文案撰寫者，以簡潔有力和乾式幽默風格聞名。
目標是作為該領域的專家，精煉並決定出唯一最佳的文案。
每次回應僅提供一個提案。
你全神貫注於當前的目標。
不要浪費時間於閒聊。
在完善構想時，請考慮各種建議。
"""

TASK = "a slogan for a new line of electric cars."


async def main():
    ai_agent_settings = AzureAIAgentSettings()

    async with (
        DefaultAzureCredential() as creds,
        AzureAIAgent.create_client(credential=creds) as client,
    ):
        # 1. Create the reviewer agent on the Azure AI agent service
        reviewer_agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name=REVIEWER_NAME,
            instructions=REVIEWER_INSTRUCTIONS,
        )

        # 2. Create a Semantic Kernel agent for the reviewer Azure AI agent
        agent_reviewer = AzureAIAgent(
            client=client,
            definition=reviewer_agent_definition,
        )

        # 3. Create the copy writer agent on the Azure AI agent service
        copy_writer_agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name=COPYWRITER_NAME,
            instructions=COPYWRITER_INSTRUCTIONS,
        )

        # 4. Create a Semantic Kernel agent for the copy writer Azure AI agent
        agent_writer = AzureAIAgent(
            client=client,
            definition=copy_writer_agent_definition,
        )

        # 5. Place the agents in a group chat with a custom termination strategy
        chat = AgentGroupChat(
            agents=[agent_writer, agent_reviewer],
            termination_strategy=ApprovalTerminationStrategy(agents=[agent_reviewer], maximum_iterations=10),
        )

        try:
            # 6. Add the task as a message to the group chat
            await chat.add_chat_message(message=TASK)
            print(f"# {AuthorRole.USER}: '{TASK}'")
            # 7. Invoke the chat
            async for content in chat.invoke():
                print(f"# {content.role} - {content.name or '*'}: '{content.content}'")
        finally:
            # 8. Cleanup: Delete the agents
            await chat.reset()
            await client.agents.delete_agent(agent_reviewer.id)
            await client.agents.delete_agent(agent_writer.id)

        """
        Sample Output:
        # AuthorRole.USER: 'a slogan for a new line of electric cars.'
        # AuthorRole.ASSISTANT - CopyWriter: '"Charge Ahead: Drive the Future."'
        # AuthorRole.ASSISTANT - ArtDirector: 'This slogan has a nice ring to it and captures the ...'
        # AuthorRole.ASSISTANT - CopyWriter: '"Plug In. Drive Green."'
        ...
        """


if __name__ == "__main__":
    asyncio.run(main())
