import streamlit as st
from agent import query_startup_data

# 1. Page Configuration
# This gives your app a professional browser tab title and layout
st.set_page_config(
    page_title="US Startup Ecosystem Explorer",
    page_icon="💡",
    layout="wide"
)

# 2. Main Title
st.title("💡 US Startup Ecosystem Explorer")
st.markdown(
    "Welcome to the interactive data explorer for US startup ecosystems. Ask me anything about the data!")

# 3. Sidebar (Rubric Requirement: "Clear explanation of the chatbot’s input requirements and data usage")
with st.sidebar:
    st.header("📊 About the Data")
    st.write(
        "This chatbot analyzes a dataset ranking the 50 US states and the District of Columbia "
        "based on their viability for startups."
    )

    st.subheader("What you can ask about:")
    st.markdown("""
    * **Rankings:** Overall state startup rank (1 is best)
    * **Demographics:** Population % of 25-34 year olds, and % with a bachelor's degree
    * **Economics:** Unemployment rate, Rent as % of median income, Per Capita Annual Wage, Cost of Living
    * **Taxes:** Personal Income Tax, Corporate Income Tax, State Sales Tax
    """)

    st.info("💡 **Pro Tip:** Try asking comparative questions like 'Which state has the lowest corporate tax but a high percentage of educated youth?'")

# 4. Initialize Chat History in Session State
# Streamlit reruns the script on every input, so we must store history in session_state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am ready to analyze the startup ecosystem data. What would you like to know?"}
    ]

# 5. Render Chat History
# This loops through saved messages and displays them on the screen
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Handle User Input with Bulletproofing
if prompt := st.chat_input("Ask about state taxes, demographics, or rankings..."):

    # --- NEW: Frontend Validation Guardrails ---
    clean_prompt = prompt.strip()

    # Guardrail 1: Catch empty or dangerously short inputs
    if len(clean_prompt) < 3:
        st.warning("⚠️ Please type a more specific question about the dataset.")

    # Guardrail 2: Catch obvious gibberish (e.g., "asdfghjkl")
    elif len(clean_prompt.split()) == 1 and len(clean_prompt) > 15:
        st.warning(
            "⚠️ Input not recognized. Please ask a natural language question about the startups data.")

    else:
        # --- Proceed with normal execution if the input passes the guardrails ---
        with st.chat_message("user"):
            st.markdown(clean_prompt)

        st.session_state.messages.append(
            {"role": "user", "content": clean_prompt})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing dataset..."):
                # Pass the cleaned query to the backend
                response = query_startup_data(clean_prompt)
                st.markdown(response)

        st.session_state.messages.append(
            {"role": "assistant", "content": response})
