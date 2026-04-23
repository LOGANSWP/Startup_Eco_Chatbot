import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables (API Key)
load_dotenv()

# Load the cleaned dataset
DATA_PATH = "data/best_state_for_startup.csv"
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    df = None
    print(f"Error: Could not find data file at {DATA_PATH}")


def query_startup_data(user_query: str) -> str:
    """
    This function will receive the user's string query from app.py.
    For now, it returns a placeholder string. 
    We will add the LangChain Pandas Agent logic here next.
    """
    if df is None:
        return "Error: Dataset not loaded."

    # Placeholder logic to prove frontend/backend connection
    return f"Backend received your query: '{user_query}'. The dataset has {len(df)} rows ready for analysis."
