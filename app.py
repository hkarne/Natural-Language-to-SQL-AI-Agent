import streamlit as st
import pandas as pd
from agent_logic import run_conversation 

# --- 1. Page Configuration ---
st.set_page_config(page_title="Google AI SQL Agent", page_icon="✨", layout="wide")

# --- 2. Sidebar Content ---
with st.sidebar:
    st.title("✨ Google AI SQL Agent")
    st.write("Welcome! This application uses an AI agent to answer questions about a company database by writing and executing SQL queries for you.")
    
    st.info("The agent has access to the following database schema. Try asking questions about it!")
    
    # Display the database schema in a more readable format
    st.code("""
Table: employees
Columns: 
- employee_id (INT)
- full_name (VARCHAR)
- department_id (INT)
- job_title (VARCHAR)
- salary (DECIMAL)
    """, language="sql")

    st.write("---")
    # NEW: Add a button to clear the chat history
    if st.button("New Chat"):
        st.session_state.messages = []
        st.rerun() # Rerun the app to clear the screen

    st.write("Built with [Streamlit](https://streamlit.io/) and [Google AI](https://ai.google/).")


# --- 3. Caching ---
# This caching is kept from the previous version
@st.cache_data
def get_cached_agent_response(question: str):
    """Wraps the run_conversation function to cache its results."""
    return run_conversation(question)

# --- 4. Main Page Content ---
st.header("Ask Your Database a Question")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Show a welcome message and example prompts if the chat is new
if not st.session_state.messages:
    st.subheader("Examples")
    # NEW: Use columns for a cleaner layout of examples
    col1, col2 = st.columns(2)
    with col1:
        st.info("Who has the highest salary?")
        st.info("What are the distinct job titles?")
    with col2:
        st.info("Count the number of employees in each department.")
        st.info("Show me the full name and salary of the top 3 highest paid employees.")


# Display chat history
for message in st.session_state.messages:
    # NEW: Use a container with a border for each message
    with st.container(border=True):
        with st.chat_message(message["role"]):
            # Check if content is a dataframe and render it, otherwise use markdown
            if isinstance(message["content"], pd.DataFrame):
                st.dataframe(message["content"])
            else:
                st.markdown(message["content"])

# --- 5. User Input Handling ---
user_question = st.chat_input("Ask something like: 'Who has the highest salary?'")

if user_question:
    # Append and display the user's message in a container
    with st.container(border=True):
        with st.chat_message("user"):
            st.markdown(user_question)
    st.session_state.messages.append({"role": "user", "content": user_question})

    # Get the agent's response
    with st.spinner("The Google AI agent is thinking..."):
        response_data = get_cached_agent_response(user_question)

        # Append and display the assistant's response in a container
        with st.container(border=True):
            with st.chat_message("assistant"):
                if "error" in response_data:
                    error_message = f"An error occurred: {response_data['error']}"
                    st.error(error_message)
                    st.session_state.messages.append({"role": "assistant", "content": error_message})
                
                elif "results" in response_data:
                    st.success("Query executed successfully!")

                    df = pd.DataFrame(response_data["results"], columns=response_data["columns"])
                    
                    # NEW: Add a metric to show the number of results found
                    st.metric(label="Rows Returned", value=len(df))
                    
                    st.dataframe(df)
                    st.session_state.messages.append({"role": "assistant", "content": df})
