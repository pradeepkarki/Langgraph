import requests

"""
╔════════════════════════════════════════════════════════════════════════════╗
║           LANGGRAPH CONCEPTS - MANUAL IMPLEMENTATION                       ║
╠════════════════════════════════════════════════════════════════════════════╣
║ CONCEPT      │ YOUR CODE              │ PURPOSE                            ║
╠══════════════╪════════════════════════╪════════════════════════════════════╣
║ State        │ state = {              │ Shared data structure for the flow  ║
║              │   "messages": []       │ Persists across all nodes          ║
║              │ }                      │                                    ║
╠══════════════╪════════════════════════╪════════════════════════════════════╣
║ Node         │ user_node()            │ Processes & stores user input      ║
║              │ llm_node()             │ Calls LLM API, stores response     ║
║              │ code_node()            │ Simulated tool/code executor       ║
╠══════════════╪════════════════════════╪════════════════════════════════════╣
║ Router       │ router()               │ Decision logic: routes to nodes    ║
║              │                        │ based on state content             ║
╠══════════════╪════════════════════════╪════════════════════════════════════╣
║ Execution    │ run_agent()            │ Orchestrates flow: user→router→node║
║              │                        │ Returns final state with messages  ║
╠══════════════╪════════════════════════╪════════════════════════════════════╣
║ LLM Call     │ call_llm()             │ Raw HTTP request to OpenAI API     ║
║              │                        │ Returns full JSON response         ║
╠══════════════╪════════════════════════╪════════════════════════════════════╣
║ Parsing      │ extract_text()         │ Extracts text from nested response ║
║              │                        │ Path: ["choices"][0]["message"]... ║
╚══════════════╧════════════════════════╧════════════════════════════════════╝
"""

# 🔹 CONFIG
API_KEY = "YOUR_API_KEY"
BASE_URL = "http://localhost:11434/v1/chat/completions"
MODEL = "qwen3:0.6b"   # or llama3 via Groq/Together

# curl http://localhost:11434/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -d '{
#     "model": "qwen3:0.6b",
#     "messages": [
#       {"role": "user", "content": "Hello"}
#     ]
#   }'

# 🔹 1. RAW LLM CALL (NO WRAPPER)
def call_llm(messages):
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(BASE_URL, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.text}")

    return response.json()


# 🔹 2. EXTRACT RESPONSE (MANUAL PARSING)
def extract_text(res):
    """
    Extracts assistant's text from OpenAI API response.
    
    RESPONSE STRUCTURE:
    ╔════════════════════════════════════════════════════════════════╗
    ║ PATH                              │ VALUE / TYPE               ║
    ╠═══════════════════════════════════╪════════════════════════════╣
    ║ res["choices"]                    │ [List of choice objects]   ║
    ║ res["choices"][0]                 │ {First/only choice}        ║
    ║ res["choices"][0]["message"]      │ {Message object}           ║
    ║ res["choices"][0]["message"]      │ {"role": "assistant",      ║
    ║       ["content"]                 │  "content": "..."}         ║
    ╚═══════════════════════════════════╧════════════════════════════╝
    """
    return res["choices"][0]["message"]["content"]


# 🔹 3. STATE (LIKE LANGGRAPH STATE)
def init_state():
    return {
        "messages": []
    }


# 🔹 4. USER NODE
def user_node(state, user_input):
    state["messages"].append({
        "role": "user",
        "content": user_input
    })
    return state


# 🔹 5. LLM NODE
def llm_node(state):
    res = call_llm(state["messages"])
    content = extract_text(res)

    state["messages"].append({
        "role": "assistant",
        "content": content
    })

    return state


# 🔹 6. SIMPLE ROUTER (AGENT-LIKE)
def router(state):
    last_msg = state["messages"][-1]["content"].lower()

    if "code" in last_msg:
        return "code_node"
    else:
        return "llm_node"


# 🔹 7. OPTIONAL: CODE NODE (SIMULATED TOOL)
def code_node(state):
    state["messages"].append({
        "role": "assistant",
        "content": "Here is a simple Python example:\n\nprint('Hello World')"
    })
    return state


# 🔹 8. RUN FLOW (GRAPH EXECUTION)
def run_agent(user_input):
    state = init_state()

    # Step 1: user input
    state = user_node(state, user_input)

    # Step 2: routing
    route = router(state)

    # Step 3: execute node
    if route == "llm_node":
        state = llm_node(state)
    elif route == "code_node":
        state = code_node(state)

    return state


# 🔹 9. MAIN
if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        state = run_agent(user_input)

        print("\nAssistant:", state["messages"][-1]["content"])
        
        
        
