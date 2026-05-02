from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",  # local
    api_key="dummy"  # not needed for local
)

def llm_call_sdk(client):
    return client.chat.completions.create(
    model="qwen3:0.6b",
    messages=[{"role": "user", "content": "Hello"}]
)
    
if __name__ == "__main__":
    
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break
        response = llm_call_sdk(client)

        print(response)