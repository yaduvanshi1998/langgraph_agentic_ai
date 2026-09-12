from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

load_dotenv()


if os.environ['OPENAI_API_KEY']:
    print("API key is set")
else:
    print("API key not set")

# 1. create llm with open ai model.

llm = ChatOpenAI(model="gpt-5-nano", temperature=0.3)
# Ask question directly to llm 
# response = llm.invoke("who is lendeavor?").content
# print(response)

# 2. Create Graph
# 2.1. create graph schema - this will remain constant for you node.

class Graph_schema(TypedDict):
    name:str
    message:str

# 2.2 Create Node/function

def greetings(state:Graph_schema):
    name=state['name']
    message=state['message']

    response = llm.invoke(f"{name}.{message}").content

    state['message'] = f" your question was {message}, here is my response: {response}"

    return state

# 2.3 Create graph with graph schema, node, edge

graph = StateGraph(Graph_schema)

graph.add_node('greetings_node', greetings)
graph.add_edge(START, 'greetings_node')
graph.add_edge('greetings_node', END)

# 2.4 compile the and invoke it

graph_compiler = graph.compile()
print(graph_compiler.get_graph().draw_mermaid())

llm_response = graph_compiler.invoke({'name':'chandan', 'message':'How are you doing?'})

print(llm_response)

