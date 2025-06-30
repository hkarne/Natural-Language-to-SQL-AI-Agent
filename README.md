# 🌟 Natural Language to SQL AI Agent

**Natural Language to SQL AI Agent** is an intelligent full-stack application that translates plain English questions into executable SQL queries. With a clean web interface, users can ask questions about an employee database and get instant answers—no SQL knowledge required!

---

## 🚀 Key Features

- **Natural Language Interface:** Ask complex questions in plain English.
- **SQL Generation:** Powered by Google’s AI Platform for accurate SQL translation.
- **Interactive UI:** Built with Streamlit for a seamless user experience.
- **Schema Awareness:** The agent uses your database schema for more precise queries.
- **Security:** API keys are protected using environment variables.

---

## ✨ Example in Action

> **Q:** What is the highest salary?  
> **A:** [Returns the highest salary from your database.]

---

## ⚙️ How It Works

1. **User Input:** Enter your question in the Streamlit web app (e.g., _“How many employees are in the engineering department?”_).
2. **Agent Processing:** The app captures your question and sends it to the core logic.
3. **LLM Translation:** The agent builds a prompt (including your schema and question) and sends it to Google’s AI model.
4. **SQL Execution:** The returned SQL query is run against your database.
5. **Display Results:** Answers are shown in the web interface.

---

## 🗄️ Database Schema

The agent works with an `employees` table structured as follows:

- `employee_id` (**INT**)
- `full_name` (**VARCHAR**)
- `department_id` (**INT**)
- `job_title` (**VARCHAR**)
- `salary` (**DECIMAL**)

---

## 🏁 Getting Started

### **Prerequisites**
- Python 3.9 or higher
- Git

### **1. Clone the Repository**
```bash
git clone https://github.com/hkarne/Natural-Language-to-SQL-AI-Agent.git
cd Natural-Language-to-SQL-AI-Agent
```

### **2. Create a Virtual Environment**
**For Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 💡 Sample Question

> _What is the average salary in the 'Engineering' department?_

---

Enjoy querying your database the easy way!
