# pip install langchain-groq => precisa instalar
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
# from langchain_groq import ChatGroq

load_dotenv()

model = ChatOpenAI(model = "gpt-4o", temperature = 0.1)
# model = ChatGroq(model = "llama-3.1-8b-instant", temperature = 0.1)

# O CHatModel é um componente LangChain então ele possui o protocolo invoke()

resposta = model.invoke("Olá como você está e o que você é capaz de fazer?")

print("--------RESPOSTA AIMessage:---------")
print(resposta)
print("-------------------------------------")

print("--------RESPOSTA Somente Texto:------")
print(resposta.content)
print("-------------------------------------")

