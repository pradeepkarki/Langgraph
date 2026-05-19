from typing import TypedDict, List, Union
# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END, START
from IPython.display import Image, display, JSON
from sqlalchemy import union

"""
chatbot with memory
"""
class AgentState(TypedDict):
    messages:List[Union[HumanMessage,AIMessage,ToolMessage]]
    
    
# Use local Ollama model
llm = ChatOllama(model="qwen3:0.6b")  



def chat_bot(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    #print("LLM Response:raw", response)
    state["messages"].append(AIMessage(content=response.content))
    print("LLM Response:", response.content )
    print("current state messages:", state["messages"])
    return state


conversation_history= []


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


#invoke

while user_input.lower() not in ["exit", "quit"]:
     conversation_history.append(HumanMessage(content=user_input))
     response = app.invoke({"messages": conversation_history})
     print("AI:", response["messages"][-1].content)
     conversation_history.append(AIMessage(content=response["messages"][-1].content))
     #print("conversation_history:", conversation_history)
     user_input = input("You: ")


#print("Final Response:", response)

