from langchain_ollama import ChatOllama

llm = ChatOllama(model="ipe")
response = llm.invoke("Tell me about partial functions in Python")
print(response.content)
