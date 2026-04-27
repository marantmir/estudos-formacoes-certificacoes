from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import HumanMessage



"""Em nossos tutoriais utilizamos normalmente a API da Open AI, conforme abaixo: """

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0.2,
)

resposta = model.invoke([HumanMessage(content="Olá como você está?")])


print("============== IMPRIMINDO A RESPOSTA =================================")
print(resposta.content)
print("======================================================================")

# Para utilizar outros serviços você precisará substituir o ChatModel pelo correspondente que deseja utilizar.
# Você pode encontrar todas as integrações permitidas em: https://python.langchain.com/docs/integrations/chat/

"""Exemplo Usando a API Groq. => https://console.groq.com/keys """

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
)

resposta = model.invoke([HumanMessage(content="Olá como você está?")])

print("============== IMPRIMINDO A RESPOSTA =================================")
print(resposta.content)
print("======================================================================")


"""Exemplo Usando a API Google. => https://ai.google.dev/ """

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.2,
)

resposta = model.invoke([HumanMessage(content="Olá como você está?")])

print("============== IMPRIMINDO A RESPOSTA =================================")
print(resposta.content)
print("======================================================================")


