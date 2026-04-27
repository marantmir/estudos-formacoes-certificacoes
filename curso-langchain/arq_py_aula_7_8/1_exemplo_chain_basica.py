from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI

# Carregar as chas APIs presentes no arquivo .env
load_dotenv()

# Instancias um chatmodel para comunicarmos com os modelos LLMs
model = ChatOpenAI(model="gpt-4o", temperature=0.5)

# Definindo o prompt de comunicação - adotamos aqui um estilo chat prompt
# template, uma vez que estamos usando o modelo do tipo chat.

prompt_sistema = """Você é um assistente especialista em criar conteúdo para o twitter e tem como objetivo \
criar os melhores tweets virais sobre o tema que o usuário te passar. Seja criativo e atenda ao padrão de 280 caracteres do \
twitter.
"""

prompt_template = ChatPromptTemplate(
    [
        ("system", prompt_sistema),
        ("human", "Crie um total de {numero_de_publicacoes} tweets sobre o tema {input_tema}."),
    ]
)

# Crie a cadeia combinada usando LangChain Expression Language (LCEL)
chain = prompt_template | model | StrOutputParser()


# Executamos nossa chain
result = chain.invoke({"numero_de_publicacoes": 3, "input_tema": "tecnologia"})

# Imprimimos a saída.
print(result)