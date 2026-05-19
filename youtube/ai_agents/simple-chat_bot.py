from typing import TypedDict, List, Optional
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END, START
from IPython.display import Image, display, JSON


class AgentState(TypedDict):
    messages:List[HumanMessage]
    
    
# Use local Ollama model
llm = ChatOllama(model="qwen3:0.6b")  



def chat_bot(state: AgentState) -> AgentState:
   response = llm.invoke(state["messages"])
   #print("LLM Response:raw", response)
   print("LLM Response:", response.content )
   return state


 #graph
 
graph = StateGraph(AgentState)

#nodes
graph.add_node("chatbot", chat_bot)

#edges
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END) 

#compile
app = graph.compile() 


#input
user_input = input("You: ")

display(Image(app.get_graph(xray=True).draw_mermaid_png()))

#invoke

while user_input.lower() not in ["exit", "quit"]:
     response = app.invoke({"messages": [HumanMessage(content=user_input)]})
     user_input = input("You: ")


#print("Final Response:", response)

