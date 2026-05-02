from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from typing import TypedDict, List
from langchain_core.messages import HumanMessage

# 🔹 LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# 🔹 TOOL
def get_weather(city: str) -> str:
    return f"The weather in {city} is 30°C and sunny"

tools = [get_weather]

llm_with_tools = llm.bind_tools(tools)

# 🔹 STATE
class State(TypedDict):
    messages: List


# 🔹 NODE
def llm_node(state: State):
    res = llm_with_tools.invoke(state["messages"])
    return {"messages": state["messages"] + [res]}


# 🔹 BUILD GRAPH
builder = StateGraph(State)
builder.add_node("llm", llm_node)
builder.set_entry_point("llm")
builder.set_finish_point("llm")

graph = builder.compile()


# 🔹 RUN
result = graph.invoke({
    "messages": [HumanMessage(content="What is weather in Pune?")]
})

print(result["messages"][-1].content)