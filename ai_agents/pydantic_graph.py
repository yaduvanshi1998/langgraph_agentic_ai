# PYDANTIC - used for data validation and data parsing

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END

load_dotenv()


if os.environ['OPENAI_API_KEY']:
    print("API key is set")
else:
    print("API key not set")

# 1. create llm with open ai model.

llm = ChatOpenAI(model="gpt-5-nano", temperature=0.3)

# 2. create the graph schema

class Graph_schema(BaseModel):
    topic: str = Field(description="The topic for linkedin post") # since we provided field it becomes a mandatory field
    post: str = Field(description="The created linkedin post")
    curated_post: str = Field(description="The fine tunned linkedin post")

# you can even ignore creating obj
schema_obj = Graph_schema(
    topic="LangGraph",
    post="Learning LangGraph",
    curated_post="Currently learning LangGraph and building AI agents!"
) 

# 3. Function/node to create the linkedin post

def create_post(state:Graph_schema):
    topic = state.topic # sicne we are using pydantic schema not normal schema
    #state.model_dump() # this is will pydantic schema to json / dict format 
    #topic = state['topic'] # after conversion of state, you can use this way to get topic

    post = state.post

    response = llm.invoke(f"{topic}").content

    state.post = response 

    return state

# 4. Function/node to create the curated/fine tuned linkedin post

def curated_post(state:Graph_schema):

    post = state.post

    updated_response = llm.invoke(f"{post}").content

    state.curated_post = updated_response 

    return state

# 5. crate the graph using stategraph, add the nodes and edges

graph = StateGraph(Graph_schema)

graph.add_node("linkedin_post", create_post)
graph.add_node("updated_linkedin_post", curated_post)
graph.add_edge(START,"linkedin_post")
graph.add_edge("linkedin_post", "updated_linkedin_post")
graph.add_edge("updated_linkedin_post", END)

# 6. compile the graph and invke the compiled graph

graph_compiler = graph.compile()
print(graph_compiler.get_graph().draw_mermaid())

res = graph_compiler.invoke({
    "topic":"generate the linkedin post for langgraph certification completion from udemy.",
    "post":"",
    "curated_post":""
})

print(res)