
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

model = ChatOpenAI(model = "gpt-4o", temperature = 0.1)

## Criando a conversa. Lembrando que os ChatModels recebem como entrada uma lista de mensagem. Assim o LangChain
# automaticamente converte isso na estrutura que o modelo LLM precisa receber para responder.

# Forma 1 de escrever:
mensagens = [
			 SystemMessage(content="Você é um especialista em astrofísica."),
			 HumanMessage(content="Qual a distancia do sol até a terra?"),
			 AIMessage(content="O Sol está a 49.600.000 km de distância da Terra."),
			 HumanMessage(content="E a distância da terra até marte?"),
]

# Forma 2 de escrever:
# mensagens = [
# 			 ("system", "Você é um especialista em astrofísica."),
# 			 ("user", "Qual a distancia do sol até a terra?"),
# 			 ("assistant", "O Sol está a&nbsp;49.600.000 km de distância da Terra."),
#            ("user", "E a distância da terra até marte?"),
# ]

# Como a entrada do usuário é a ultima mensagem da lista, você pode dá invoke usando a lista de pensagens contendo o histórico de conversação.
resposta = model.invoke(mensagens)

print("--------RESPOSTA AIMessage:---------")
print(resposta)
print("-------------------------------------")

print("--------RESPOSTA Somente Texto:------")
print(resposta.content)
print("-------------------------------------")