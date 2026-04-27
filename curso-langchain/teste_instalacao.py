# Chat Model Documents: https://python.langchain.com/docs/integrations/chat/

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Carregando as variaveis de '.env'
load_dotenv()

# Chama a API do modelos da Open IA.
model = ChatOpenAI(model="gpt-4o")

# Executa a chamada ao modelo
result = model.invoke("Este é um teste. Se você recebeu a requisição responda 'Teste OK'.")
print(result)