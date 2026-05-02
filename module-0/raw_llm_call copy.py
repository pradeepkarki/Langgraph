
# 🔹 CONFIG
import requests

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



# 🔹 9. MAIN
def call_llm(BASE_URL, MODEL, user_input):
    return requests.post(BASE_URL, headers={
            "Content-Type": "application/json"
        }, json={
            "model": MODEL,
            "messages": [   {"role": "user", "content": user_input}]
        }).json()

if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        res = call_llm(BASE_URL, MODEL, user_input)
        
        print("\nFull Response:", res)  # Print the full JSON response for debugging

        content = res["choices"][0]["message"]["content"]

        print("\nAssistant:", content)
        