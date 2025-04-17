# Copyright (c) Microsoft. All rights reserved.

import asyncio

from azure.ai.projects.models import CodeInterpreterTool
from azure.identity.aio import DefaultAzureCredential

from semantic_kernel.agents import AzureAIAgent, AzureAIAgentSettings, AzureAIAgentThread
from semantic_kernel.contents import AuthorRole

"""
以下範例展示如何建立一個簡單的 Azure AI agent，
該 agent 使用程式碼解釋器工具來回答程式編寫問題。
"""

TASK = "Use code to determine the values in the Fibonacci sequence that that are less then the value of 101."


async def main() -> None:
    ai_agent_settings = AzureAIAgentSettings()

    async with (
        DefaultAzureCredential() as creds,
        AzureAIAgent.create_client(credential=creds) as client,
    ):
        # 1. Create an agent with a code interpreter on the Azure AI agent service
        code_interpreter = CodeInterpreterTool()
        agent_definition = await client.agents.create_agent(
            model=ai_agent_settings.model_deployment_name,
            tools=code_interpreter.definitions,
            tool_resources=code_interpreter.resources,
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
            print(f"# User: '{TASK}'")
            # 4. Invoke the agent for the specified thread for response
            async for response in agent.invoke(messages=TASK, thread=thread):
                if response.role != AuthorRole.TOOL:
                    print(f"# Agent: {response}")
                thread = response.thread
        finally:
            # 6. Cleanup: Delete the thread and agent
            await thread.delete() if thread else None
            await client.agents.delete_agent(agent.id)

        """
        Sample Output:
        # User: 'Use code to determine the values in the Fibonacci sequence that that are less then the value of 101.'
        # Agent: # Function to generate Fibonacci sequence values less than a given limit
        def fibonacci_less_than(limit):
            fib_sequence = []
            a, b = 0, 1
            while a < limit:
                fib_sequence.append(a)
                a, b = b, a + b
            a, b = 0, 1
            while a < limit:
                fib_sequence.append(a)
            a, b = 0, 1
            while a < limit:
            a, b = 0, 1
            a, b = 0, 1
            while a < limit:
                fib_sequence.append(a)
                a, b = b, a + b
            return fib_sequence

        Generate Fibonacci sequence values less than 101
        fibonacci_values = fibonacci_less_than(101)
        fibonacci_values
        # Agent: The values in the Fibonacci sequence that are less than 101 are:

        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
        """


if __name__ == "__main__":
    asyncio.run(main())
