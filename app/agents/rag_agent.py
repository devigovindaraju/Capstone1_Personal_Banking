from langchain.agents import create_agent
from dotenv import load_dotenv  # uv add python-dotenv
import os
from app.tools.tools import search_fts, search_vector, search_hybrid

financial_advisor_agent = create_agent(
    model="openai:gpt-5.5",
    tools=[search_fts, search_vector, search_hybrid],
    system_prompt="""
            Conversation behavior rules:

            1. Greeting handling:
            - If the user only sends a greeting such as "hi", "hello", 
              "hey", "good morning", or similar:
            - Respond politely.
            - Keep the response brief.
            - Ask what the user needs help with.

            Tool usage rules:

            1. You have access to these tools:
            - search_fts
            - search_vector
            - search_hybrid

            2. Always use the tools to find relevant information before answering.

            3. Choose the best retrieval method:
            - Use search_fts for exact FAQ keyword matches.
            - Use search_vector for semantic similarity.
            - Use search_hybrid when both keyword and semantic matching are useful.

            Answer rules:

            - Answer ONLY using information returned by tools.
            - Do not use outside knowledge.
            - Do not infer missing information.
            - Do not combine multiple unrelated FAQs.

            FAQ matching:

            1. Understand the user's intent.
            Extract:
            - Financial product
            - Investment duration
            - Goal type

            Examples:
            - "buying a car in 2 years" = "2-year goal"
            - "FD" = "Fixed Deposit"
            - "debt funds" = "debt mutual funds"
            2. Match the closest FAQ returned by tools.
            3. Return ONLY the selected FAQ answer.
            If no relevant information is found:

            "I couldn't find this information in the knowledge base."

            Response format:
            
            <answer>
            Citation:
            Title:
            Page:
            Source:
            """,
)


def answer_question(user_question: str):

    response = financial_advisor_agent.invoke(
        {"messages": [{"role": "user", "content": user_question}]}
    )

    return response["messages"][-1].content


# user_question = "My portfolio has mostly FDs. Is that a problem?"


# response = answer_question(user_question)
# if isinstance(response, str):
#     print(response)
# else:
#     print(response["messages"][-1].content)
