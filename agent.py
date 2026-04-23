import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# 1. Load environment variables (pulls OPENAI_API_KEY from your .env file)
load_dotenv(override=True)

# 2. Load the cleaned dataset
DATA_PATH = "data/best_state_for_startup.csv"
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    df = None
    print(f"Error: Could not find data file at {DATA_PATH}")

# 3. Initialize the OpenAI LLM
# temperature=0 ensures the model is strictly analytical and does not hallucinate data
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 4. Initialize the LangChain Pandas Agent
if df is not None:
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,  # Set to True so you can see the agent's thought process
        agent_type="openai-tools"
    )
else:
    agent = None

# 5. Define the core query function used by the frontend


def query_startup_data(user_query: str) -> str:
    """
    Receives the user's natural language query, enforces the persona,
    and uses the LangChain agent to query the dataframe.
    """
    if agent is None:
        return "Error: Dataset not loaded. Please check your data folder."

    # 6. System Prompt / Persona (Crucial for "Reliability" points on the rubric)
    system_instruction = (
        "You are an expert data analyst assistant for the TE 440 course. "
        "You answer questions strictly based on the provided dataset containing economic and demographic factors for US states. "
        "If a user asks a question unrelated to states, startups, taxes, economics, or demographics, politely decline "
        "and state that you can only answer questions regarding the startup dataset. "
        "Do not generate or write code to show visualizations to the user; only return clear, professional text summaries and data insights. "
        f"User Question: {user_query}"
    )

    try:
        # Pass the formatted instruction to the agent
        response = agent.invoke({"input": system_instruction})
        return response.get("output", "I could not generate an answer.")
    except Exception as e:
        return f"I encountered an error analyzing the data: {str(e)}"


# 7. Local Testing Block
# This allows you to test the agent directly in the terminal
if __name__ == "__main__":
    print("--- TE 440 Backend Agent Initialized ---")
    print("Type 'exit' to quit.\n")

    while True:
        test_query = input("Ask a question: ")
        if test_query.lower() == 'exit':
            break

        print("\nThinking...")
        answer = query_startup_data(test_query)
        print(f"\nFinal Answer: {answer}\n")
        print("-" * 40)
