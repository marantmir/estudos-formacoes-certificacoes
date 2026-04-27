from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


"""Exemplo Usando a API OLLAMA = Local. => https://ollama.com/search """

model = ChatOllama(
    base_url="http://localhost:11434",
    model = "deepseek-r1",
    temperature = 0.3,
    num_predict = 1000, # mesmo funcionamento do max token
)

resposta = model.invoke([HumanMessage(content="Olá como você está?")])

print("============== IMPRIMINDO O TIPO DE OBJETIVO QUE RETORNA =============")
print(type(resposta))
print("======================================================================")
print("============== IMPRIMINDO O OBJETO ===================================")
print(resposta)
print("======================================================================")
print("============== IMPRIMINDO A RESPOSTA =================================")
print(resposta.content)
print("======================================================================")
print("============== IMPRIMINDO O TOTAL DE TOKENS USADOS ===================")
print(resposta.usage_metadata)
print("======================================================================")

