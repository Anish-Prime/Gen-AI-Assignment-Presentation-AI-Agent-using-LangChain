# Beyond the Chatbot: Orchestrating AI Agents with LangChain

This repository contains the live demonstration code for my Generative AI presentation on **Multi-Agent Systems and LangChain**. 

Rather than a standard, static LLM, this project features a fully functional **ReAct (Reasoning + Acting) Agent**. It demonstrates how a framework like LangChain can equip an open-source model with external tools to solve complex problems autonomously.

## 🚀 Features

* **Tool Integration:** The agent is equipped with live internet access via the `Wikipedia API` and exact mathematical reasoning via a `Calculator` tool.
* **Open-Source Brain:** Powered by Meta's `Llama-3.3-70b-versatile` running on the blazing-fast Groq inference engine.
* **A/B Testing Toggle:** Features a live toggle switch to instantly swap between a "Raw Chatbot" (no tools) and the "LangChain Agent" (tools active) to demonstrate the power of agentic workflows.
* **Graceful UI:** Includes custom tool wrappers to format Wikipedia outputs cleanly in the terminal and prevent infinite reasoning loops.

## 📋 Prerequisites

To run this demonstration locally, you will need:
* **Python 3.10 to 3.12** (Note: Python 3.14+ is currently unstable with Pydantic V1).
* A free **Groq API Key** (Get one at [console.groq.com](https://console.groq.com/)).

## 🛠️ Installation & Setup

It is highly recommended to use a virtual environment (like `uv` or `venv`) to prevent dependency conflicts.

**1. Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/beyond-the-chatbot.git](https://github.com/YOUR_USERNAME/beyond-the-chatbot.git)
cd beyond-the-chatbot
```
**2. Create and activate a virtual environment (using uv):**
```bash
uv venv -p 3.11 agent_env
source agent_env/bin/activate
```
**3. Install the required dependencies:**
```bash
uv pip install langchain_groq langchain_community langchain_classic wikipedia numexpr
```
**4. Add your API Key:**
Open demo_agent.py and replace "YOUR_GROQ_API_KEY_HERE" with your actual Groq API key on Line 19.

**5. 💻 Running the Agent:**
```bash
python demo_agent.py
```
## Demonstration Guide
Once the agent is initialized, try the following flow:
1. Type toggle to switch to RAW CHATBOT mode.
2. Ask a complex math question (e.g., "What is the square root of 74849 multiplied by 13.5?"). Note the confident but likely incorrect answer.
3. Type toggle to switch to AGENT mode.
4. Ask the exact same question. Watch the agent trigger the Calculator tool, execute the math, and return the flawless answer.
5. Ask a current events question (e.g., "How old is the current Prime Minister of the UK in 2026 multiplied by 5?"). Watch it chain the Wikipedia tool and the Calculator tool together autonomously.
