import os
import sys
from langchain_openai import ChatOpenAI
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph
import time

    
def run():
    print("Input your OpenAI api key from the main filefolder KG/openai_key.txt: \n ")
    with open('openai_key.txt', 'r') as file:
        lines = file.read()
        lines = lines.strip().strip('"')
        os.environ["OPENAI_API_KEY"] = lines   # file.read()
    print(os.environ["OPENAI_API_KEY"])
    graph = Neo4jGraph(url="bolt://neo4j:7687", username="neo4j", password="12345678")  # docker
    #graph = Neo4jGraph(url="bolt://127.0.0.1:7687", username="neo4j", password="12345678")  # standalone
    chain = GraphCypherQAChain.from_llm(ChatOpenAI(temperature=0), graph=graph, verbose=True, allow_dangerous_requests=True)

    questions = [
        "How many agents in this graph?",
        "Show me all the agents with their names",
        "Show me the parameters of material al6082, and show their values and units",
        #"How many parameters in the ODE analytical model, and show me their names and value"
        ]

    for i in range(0, len(questions)):
        print("Ask a question about the three-story floor structure (or type 'exit' to quit): \n")
        time.sleep(2)
        print(questions[i])
        response = chain.invoke(questions[i])
        print(f"Response: {response['result']}\n\n\n\n\n\n\n\n\n\n\n\n")
    
    # while True:
    #     # Prompt user for input
    #     user_input = input("Ask a question about the three-story floor structure (or type 'exit' to quit): ") #  \n ->")

    #     print("output", user_input)
    
    #     # Check if the user wants to exit
    #     if user_input.lower() == 'exit':
    #         print("Exiting the loop. Goodbye!")
    #         break

    #     try:
        
    #         # Pass the user's question to chain.run() and get the response
    #         response = chain.invoke(user_input)
        
    #         # Print the response
    #         print(f"Response: {response['result']}\n\n\n\n\n\n\n\n\n\n\n\n")

    #     except Exception as e:
    #         print(f"An error occurred: {e}\n")


