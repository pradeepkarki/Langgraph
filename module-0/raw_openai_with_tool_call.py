import requests
import json

# 🔹 CONFIG
API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4o-mini"

# 🔹 TOOL DEFINITION (manual)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }
]


# 🔹 TOOL IMPLEMENTATION
def get_weather(city):
    return f"The weather in {city} is 30°C and sunny"


# 🔹 RAW LLM CALL
def call_llm(messages):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS,
        "tool_choice": "auto"
    }

    res = requests.post(BASE_URL, headers=headers, json=payload)

    if res.status_code != 200:
        raise Exception(res.text)

    return res.json()


# 🔹 EXECUTE TOOL
def execute_tool(tool_call):
    name = tool_call["function"]["name"]
    args = json.loads(tool_call["function"]["arguments"])

    if name == "get_weather":
        return get_weather(args["city"])

    return "Unknown tool"


# 🔹 AGENT LOOP
def run_agent(user_input):
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": user_input}
    ]

    while True:
        res = call_llm(messages)
        msg = res["choices"][0]["message"]

        # 🔹 If LLM wants to call tool
        if "tool_calls" in msg:
            tool_call = msg["tool_calls"][0]

            tool_result = execute_tool(tool_call)

            # Append assistant tool request
            messages.append(msg)

            # Append tool response
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": tool_result
            })

        else:
            # Final answer
            return msg["content"]


# 🔹 MAIN
if __name__ == "__main__":
    while True:
        q = input("\nYou: ")
        if q in ["exit", "quit"]:
            break

        ans = run_agent(q)
        print("\nAssistant:", ans)
        
        
# 🔥 What’s happening here

# You manually handled:
# 	•	Tool schema
# 	•	Tool execution
# 	•	Loop until final answer
# 	•	JSON parsing

# 👉 This is exactly what frameworks automate.