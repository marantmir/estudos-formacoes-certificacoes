# documentação: https://python.langchain.com/docs/concepts/output_parsers/

# Realizando as importações:
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Contextualização - Exemplo da aula anterior.

# Carregamento das variáveis de ambiente presentes em .env
load_dotenv()

# Criando o componente de langchain que iterage com os LLMs
model = ChatOpenAI(model="gpt-4o")

### Exemplo 1

prompt_template = ChatPromptTemplate([("user", "Escreva um poema em {lingua} sobre o tema: {assunto}")])

# PART 2: Criando a chain
chain1 = prompt_template | model

# PART 3: Invoke da chain passando as variáveis.
resposta1 = chain1.invoke({"lingua": "pt-br", "assunto":"frutas"})

print(type(resposta1)) # aqui será criada uma AIMessage
print("--"*50)
print(resposta1.content) # Aqui estamos acessando o conteudo da mensagem via content.
print("--"*50)

# Prática 1 - StrOutputParser
#
# E se eu quisesse pegar a saida anterior e obtê-la sem precisar acessar content? Simples usamos StrOutputParser para
# capturar a saida do LLM no formato puro de string.

from langchain_core.output_parsers import StrOutputParser

analisador_saida = StrOutputParser()

chain1_com_outputparser = prompt_template | model | analisador_saida

resposta2 = chain1_com_outputparser.invoke({"lingua": "pt-br", "assunto":"frutas"})

print(type(resposta2)) # Tipo 'str'
print("--"*50)
print(resposta2) # agora resposta não é mais uma 'AIMessage'
print("--"*50)


