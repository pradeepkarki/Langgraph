from langgraph.graph import StateGraph
from langchain_community.chat_models import ChatOllama

# Use local Ollama model
llm = ChatOllama(model="llama3")

# Define state
class State(dict):
    pass

# Node function
def chatbot(state):
    response = llm.invoke(state["input"])
    return {"output": response.content}

# Build graph
graph = StateGraph(State)

graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.set_finish_point("chatbot")

app = graph.compile()

# Run
if __name__ == "__main__":
    result = app.invoke({"input": "Explain LangGraph in simple terms"})
    print(result["output"])