from mcp import MCPClient
from langgraph import Graph

mongo_mcp = MCPClient("http://127.0.0.1:8000/mcp")
graph = Graph()
graph.add_tool("mongo", mongo_mcp)

response = graph.run("List top 5 students with highest math scores")
print(response)
