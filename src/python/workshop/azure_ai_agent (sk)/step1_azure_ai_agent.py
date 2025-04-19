# Copyright (c) Microsoft. All rights reserved.

import asyncio

from azure.identity.aio import DefaultAzureCredential

from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread

"""
以下範例展示如何建立一個 Azure AI agent 來回答
使用者問題。本範例說明建立 agent 的基本步驟，
並模擬與 agent 的對話。

與 agent 的互動是透過 `get_response` 方法進行，
該方法會將使用者輸入傳送給 agent，並從 agent
接收回應。對話歷史由 agent 服務自動維護，
也就是說，回應會自動與對話串(thread)關聯。
因此，客戶端程式碼不需要自行維護對話歷史。
"""


# Simulate a conversation with the agent
USER_INPUTS = [
    "Hello, I am John Doe.",
    "What is your name?",
    "What is my name?",
]


async def main() -> None:
    ai_agent_settings = AzureAIAgentSettings()

    async with (
        DefaultAzureCredential() as creds,
        AzureAIAgent.create_client(credential=creds) as client,
    ):
        # 1. Create an agent on the Azure AI agent service
        agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            name="Assistant",
            instructions="Answer the user's questions.",
        )

        # 2. Create a Semantic Kernel agent for the Azure AI agent
        agent = AzureAIAgent(
            client=client,
            definition=agent_definition,
        )

        # 3. Create a thread for the agent
        # If no thread is provided, a new thread will be
        # created and returned with the initial response
        thread: AzureAIAgentThread = None

        try:
            for user_input in USER_INPUTS:
                print(f"# User: {user_input}")
                # 4. Invoke the agent with the specified message for response
                response = await agent.get_response(messages=user_input, thread=thread)
                print(f"# {response.name}: {response}")
                thread = response.thread
        finally:
            # 6. Cleanup: Delete the thread and agent
            await thread.delete() if thread else None
            await client.agents.delete_agent(agent.id)

        """
        Sample Output:
        # User: Hello, I am John Doe.
        # Assistant: Hello, John! How can I assist you today?
        # User: What is your name?
        # Assistant: I'm here as your assistant, so you can just call me Assistant. How can I help you today?
        # User: What is my name?
        # Assistant: Your name is John Doe. How can I assist you today, John?
        """


if __name__ == "__main__":
    asyncio.run(main())
