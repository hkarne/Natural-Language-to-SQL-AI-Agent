import os
import json
from dotenv import load_dotenv
from typing import Dict, Any

from autogen import ConversableAgent, UserProxyAgent

load_dotenv()

# --- 1. LLM Configuration ---
config_list = [
    {
        "model": "gemini-1.5-flash",
        "api_key": os.getenv("GEMINI_API_KEY"),
        "api_type": "google",
    }
]

llm_config = {
    "config_list": config_list,
    "cache_seed": 42,
}

# --- 2. System Message Construction ---
PROMPT_TEMPLATE = """You are an expert Python programmer who specializes in writing scripts to query PostgreSQL databases.
Your task is to write a single, self-contained Python script to answer the user's question.

RULES:
1.  The script MUST be placed inside a ```python code block.
2.  The script MUST install its own dependencies using pip (specifically `psycopg2-binary`).
3.  The script MUST connect to the database using the following hardcoded credentials. DO NOT use environment variables from the OS.
    DB_HOST = "localhost"
    DB_PORT = {db_port}
    DB_NAME = "{db_name}"
    DB_USER = "{db_user}"
    DB_PASSWORD = "{db_password}"
4.  The script MUST print the final answer as a JSON object to standard output. The JSON object must have two keys: 'columns' (a list of column names) and 'results' (a list of lists, where each inner list is a row).
5.  Do not use any tables or columns that are not listed in the schema below.
6.  If the user asks "who" has something (e.g., "who has the highest salary"), you MUST return the `employee_id` for that record. Do not assume `first_name` or `last_name` columns exist unless they are explicitly part of the question.
7.  If the user's question cannot be answered using the schema, return an empty JSON object.

Here is the database schema:
Table: employees
Columns: employee_id (INT), full_name (VARCHAR), department_id (INT), job_title (VARCHAR), salary (DECIMAL)
"""

# --- 3. Agent & Conversation Flow Definitions ---

# The user_proxy is the agent that EXECUTES the code.
# Its termination rule is now to stop when it receives a message containing "TERMINATE".
user_proxy = UserProxyAgent(
    name="Code_Executor",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: "TERMINATE" in x.get("content", ""),
    max_consecutive_auto_reply=8,
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

# The assistant is the agent that WRITES the Python code.
assistant_agent = ConversableAgent(
    name="Python_SQL_Writer",
    llm_config=llm_config,
    system_message=PROMPT_TEMPLATE.format(
        db_port=os.getenv("DB_PORT"),
        db_name=os.getenv("DB_NAME"),
        db_user=os.getenv("DB_USER"),
        db_password=os.getenv("DB_PASSWORD"),
    ),
)

# --- NEW: Define a custom reply function for the assistant ---
# This creates the explicit "handshake" to end the conversation.
def assistant_reply_logic(recipient, messages, sender, config):
    """
    A custom reply function for the assistant agent.
    If the last message from the Code_Executor contains "exitcode: 0",
    it replies with a "TERMINATE" message to cleanly end the conversation.
    Otherwise, it falls back to the default behavior.
    """
    last_message = messages[-1]
    if "exitcode: 0" in last_message.get("content", ""):
        # If the code execution was successful, send the termination signal.
        return True, "The task is complete. TERMINATE"
    
    # Otherwise, let the agent generate a reply as usual.
    return False, None 

# Register the custom reply function.
# This tells the assistant to use our new logic for any message received from the user_proxy.
assistant_agent.register_reply(
    trigger=user_proxy,
    reply_func=assistant_reply_logic,
    position=1 # Setting a position ensures it's checked early.
)

# --- 4. Main Conversation Runner ---
def run_conversation(question: str) -> Dict[str, Any]:
    """
    This function is called by app.py. It orchestrates the conversation
    between the agents and returns the final result.
    """
    chat_result = user_proxy.initiate_chat(
        assistant_agent,
        message=f"Please write a Python script to answer this question: {question}",
        clear_history=True,
    )

    # --- FINAL PARSING LOGIC ---
    # We will search the history for the message sent by the 'Code_Executor' agent.
    for msg in reversed(chat_result.chat_history):
        # THIS IS THE CORRECTED LINE: Check for the sender's name.
        if msg.get("name") == "Code_Executor" and "exitcode: 0" in msg.get("content", ""):
            try:
                content = msg["content"]
                json_start_index = content.find('{')
                json_end_index = content.rfind('}') + 1

                if json_start_index != -1 and json_end_index != 0:
                    json_str = content[json_start_index:json_end_index]
                    return json.loads(json_str)
                else:
                    return {"error": "Found the success message, but no JSON was in it."}

            except (json.JSONDecodeError, TypeError) as e:
                return {"error": f"Could not parse JSON from agent output: {e}"}

    # Fallback error if the loop finishes without finding the message.
    last_message = chat_result.summary or "The agent failed to produce a valid script."
    return {"error": f"The agent failed to find the result in the chat history. Last message: {last_message}"}
