Natural Language to SQL AI Agent
This project is an intelligent AI agent that translates plain English questions into executable SQL queries. It provides a simple web interface where users can ask questions about an employee database, and the agent will query the database and return the answer.

This eliminates the need for users to know SQL, allowing them to retrieve complex information from a database using conversational language.

🚀 Key Features
Natural Language Interface: Ask complex questions in plain English.

SQL Generation: Leverages a Large Language Model (LLM) to intelligently convert questions into accurate SQL queries.

Interactive UI: Built with Streamlit for a clean, user-friendly web interface.

Easy Setup: Comes with scripts to set up the database and sample data.

Secure: Uses environment variables to keep your API keys safe.

⚙️ How It Works
The application follows a simple yet powerful workflow:

User Input: The user enters a question into the Streamlit web interface (e.g., "How many employees are in the engineering department?").

Agent Processing: The app.py script captures this input and passes it to the core logic in agent_logic.py.

LLM-Powered Translation: The agent constructs a detailed prompt, including the database schema and the user's question, and sends it to an LLM (like Google's Gemini or OpenAI's GPT).

SQL Execution: The LLM returns a corresponding SQL query. The agent then executes this query against the local database.

Display Results: The query results are sent back to the Streamlit frontend and displayed to the user in a clean format.

🗄️ Database Schema
The agent operates on a database created from the employee.sql file. The primary table is employees, which has the following structure:

ID (INTEGER, Primary Key)

Name (TEXT)

Department (TEXT)

Salary (INTEGER)

HireDate (DATE)

This structure allows for a wide range of questions about employee data, salaries, departments, and tenure.

🏁 Getting Started
Follow these instructions to get the project up and running on your local machine.

Prerequisites
Python 3.9 or higher

A Git client

1. Clone the Repository
First, clone the project from GitHub to your local machine:

git clone [https://github.com/hkarne/Natural-Language-to-SQL-AI-Agent.git](https://github.com/hkarne/Natural-Language-to-SQL-AI-Agent.git)
cd Natural-Language-to-SQL-AI-Agent

2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage dependencies.

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

3. Install Dependencies
Install all the required Python packages using the requirements.txt file.

pip install -r requirements.txt

4. Set Up Environment Variables
This project requires an API key for the Language Model.

Create a new file named .env in the root of the project directory.

Copy the contents of the example below into your new .env file.

Example .env file:

# Replace YOUR_API_KEY with your actual key from Google AI Studio or OpenAI
API_KEY="YOUR_API_KEY_HERE"

5. Initialize the Database
The project uses a local SQLite database. The provided employees.csv can be used to populate it. (You may need to adapt your Python scripts to create and populate an SQLite database from the CSV if they don't do so automatically).

▶️ Usage
Once the setup is complete, you can run the Streamlit application.

Make sure your virtual environment is activated.

Run the following command in your terminal:

streamlit run app.py

Your web browser should automatically open to the application's interface.

Example Questions
You can now ask the agent questions like:

"Who are the top 5 highest-paid employees?"

"Show me all employees from the 'Sales' department."

"How many people were hired in 2023?"

"What is the average salary in the 'Engineering' department?"

🛠️ Technologies Used
Backend: Python

Web Framework: Streamlit

AI/LLM Integration: LangChain (or a similar library)

Database: SQLite / PostgreSQL

Data Handling: Pandas
