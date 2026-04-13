# 1. Import the LangChain components
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool 

from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

# Setup some colors for a pretty terminal UI
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# 2. The Brain
llm = ChatGroq(
    temperature=0, 
    groq_api_key="YOUR_API_KEY", # Keep your key here!
    model_name="llama-3.3-70b-versatile" 
)

# 3. The Hands 
# First, setup the base Wikipedia tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=800)
base_wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

# Wrap Wikipedia to automatically add clean spacing and "..."
def clean_wiki(query):
    result = base_wiki.run(query)
    return f"\n{result}...\n\n"

wiki_tool = Tool(
    name="wikipedia",
    func=clean_wiki,
    description="Searches Wikipedia for current events, facts, or people."
)

# Setup the base Math tool
base_math = load_tools(["llm-math"], llm=llm)[0]

# Wrap Math to add clean spacing
def clean_math(query):
    result = base_math.run(query)
    return f"\n{result}\n\n"

math_tool = Tool(
    name="Calculator",
    func=clean_math,
    description="Useful for when you need to answer questions about math."
)

# Combine our beautifully formatted tools
tools = [wiki_tool, math_tool]

# 4. The Persona 
template = '''Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the exact following format and ALWAYS include blank lines between steps:

Question: the input question you must answer

Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)

# 5. The Orchestrator
agent = create_react_agent(llm, tools, prompt)

# 6. The Executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=5)

# 7. The Interactive Loop
agent_mode = True 

print("\n" + "="*60)
print(f"{CYAN}🤖 LANGCHAIN DEMO AGENT INITIALIZED{RESET}")
print("Type a question to ask the AI.")
print(f"Type {YELLOW}'toggle'{RESET} to turn tools ON or OFF.")
print(f"Type {YELLOW}'quit'{RESET} to close.")
print("="*60)

while True:
    try:
        mode_text = f"{GREEN}AGENT (Tools ON){RESET}" if agent_mode else f"{YELLOW}RAW CHATBOT (Tools OFF){RESET}"
        
        user_question = input(f"\n[{mode_text}] Ask a question: ")
        
        if user_question.lower() in ['quit', 'exit']:
            print(f"\n{CYAN}Shutting down agent...{RESET}")
            break
            
        if user_question.lower() == 'toggle':
            agent_mode = not agent_mode
            print(f"\n{CYAN}🔄 Switched mode!{RESET}")
            continue
            
        if not user_question.strip():
            continue
            
        if agent_mode:
            agent_executor.invoke({"input": user_question})
        else:
            print(f"\n{YELLOW}Thinking without tools...{RESET}")
            response = llm.invoke(user_question)
            print(f"\n{GREEN}Answer:{RESET} {response.content}")
        
    except KeyboardInterrupt:
        print(f"\n\n{CYAN}Force quitting agent...{RESET}")
        break

    # Who is the current Mayor of New York?
    # What is the square root of 74849 multiplied by 13.5?