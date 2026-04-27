from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_ollama import ChatOllama



# Instancias um chatmodel para comunicarmos com os modelos LLMs
model = ChatOllama(
    base_url="http://localhost:11434",
    model = "deepseek-r1",
    temperature = 0.3,
    num_predict = 1000, # mesmo funcionamento do max token
)


# Definindo o prompt de comunicação - adotamos aqui um estilo chat prompt template, uma vez que estamos usando
# o modelo do tipo chat.

prompt_sistema = """Você é um assistente especialista em criar conteúdo para o twitter e tem como objetivo \
criar os melhores tweets virais sobre o tema que o usuário te passar. Seja criativo e atenda ao padrão de 280 caracteres do \
twitter. RESPONDA EM PORTUGUÊS"""

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