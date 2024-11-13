import os
from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores.neo4j_vector import remove_lucene_chars
from langchain_core.tools import tool
from langchain_nvidia_ai_endpoints import ChatNVIDIA

from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import \
    format_to_openai_function_messages
from langchain.agents.output_parsers.openai_tools import \
    OpenAIToolsAgentOutputParser
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.pydantic_v1 import BaseModel, Field
from langchain.schema import AIMessage, HumanMessage
from langchain.tools import BaseTool
from langchain.tools.render import format_tool_to_openai_function

os.environ["NEO4J_URI"] = "bolt://127.0.0.1:7688"
os.environ["NEO4J_USERNAME"] = "neo4j"
os.environ["NEO4J_PASSWORD"] = "12345678"
graph = Neo4jGraph(refresh_schema=False)


# Set up Neo4j connection details
NEO4J_URI = "bolt://127.0.0.1:7688"  # Neo4j URI (adjust if hosted differently)
NEO4J_USER = "neo4j"                 # Neo4j username
NEO4J_PASSWORD = "12345678"     # Neo4j password

# Set up the Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Define a function to query the Neo4j database
def query_neo4j(cypher_query, parameters=None):
    with driver.session() as session:
        result = session.run(cypher_query, parameters)
        return [record.data() for record in result]


# Set up LLaMA with LangChain
llama_path = "/path/to/llama/model.bin"  # Path to your LLaMA model file
llm = LlamaCpp(model_path=llama_path)
