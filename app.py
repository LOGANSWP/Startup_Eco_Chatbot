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

# 6. Handle User Input
# st.chat_input creates the text box at the bottom of the screen
if prompt := st.chat_input("Ask about state taxes, demographics, or rankings..."):

    # Immediately display the user's message in the chat interface
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add the user's message to the session state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 7. Fetch and Display the Assistant's Response
    with st.chat_message("assistant"):
        # The spinner provides visual feedback while the LangChain agent "thinks"
        with st.spinner("Analyzing dataset..."):

            # Call the function from your agent.py file
            response = query_startup_data(prompt)

            # Display the result
            st.markdown(response)

    # Add the assistant's response to the session state so it stays on screen
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
