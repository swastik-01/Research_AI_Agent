# 🤖 Research AI Agent

This project is an advanced, conversational AI research assistant. The agent uses multiple tools, including Wikipedia and web search (Tavily), to gather information, synthesize findings, and provide structured, detailed results on any given topic.

---

## ✨ Features

-   **Conversational Memory:** Remembers the context of the conversation for follow-up questions.
-   **Multi-Tool Capability:** Utilizes different tools for different tasks (e.g., Wikipedia for facts, Tavily for recent info, ArXiv for papers).
-   **Structured Output:** Provides answers in a clean, parsed format with a summary, key points, sources, and more.
-   **Advanced Prompting:** Engineered to plan its research, execute tool calls, and synthesize the results into a cohesive analysis.
-   **Powered by Groq:** Uses high-speed LLMs from Groq for near-instant responses.

---

## 🛠️ Setup and Installation

Follow these steps to get the agent running on your local machine.

**1. Clone the Repository**
git clone [https://github.com/swastik-01/Research_AI_Agent.git](https://github.com/swastik-01/Research_AI_Agent.git)
cd Research_AI_Agent

**2. Create a Virtual Environment**

# For Windows
python -m venv .venv
.\.venv\Scripts\activate

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

**3. Install Dependencies**
pip install -r requirements.txt

**4. Create a .env File**
Create a .env file in the root of the project directory and add your API keys. This file is not committed to GitHub.

GROQ_API_KEY="your_groq_api_key_here"
TAVILY_API_KEY="your_tavily_api_key_here"


**🚀 Usage**
Once the setup is complete, simply run the main script from your terminal:

python main.py
The agent will greet you, and you can start your research by typing a topic and pressing Enter. To end the session, type exit or quit.
