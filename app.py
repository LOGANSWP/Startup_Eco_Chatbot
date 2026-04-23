import streamlit as st
from agent import query_startup_data

# 1. Page Configuration
st.set_page_config(page_title="US Startup Ecosystem Explorer", page_icon="💡")
st.title("💡 US Startup Ecosystem Explorer")

# 2. Sidebar (Fulfilling the rubric requirement to explain input/data usage)
with st.sidebar:
    st.header("About this Chatbot")
    st.write("This tool analyzes the top 50 US states (plus D.C.) to determine their viability for startups.")
    st.markdown("""
    **You can ask questions about:**
    * Unemployment Rates
    * Rent Burden
    * Youth Population & Education
    * Tax Rates (Income, Corporate, Sales)
    * Cost of Living & Annual Wages
    """)

# 3. Initialize Chat History in Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
            "content": "Hello! Ask me a question about the US startup ecosystem data."}
    ]

# 4. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle User Input
if prompt := st.chat_input("Ask about state taxes, demographics, or rankings..."):

    # Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Pass query to the backend agent and display the response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing dataset..."):
            response = query_startup_data(prompt)
            st.markdown(response)

    # Add assistant response to state
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
