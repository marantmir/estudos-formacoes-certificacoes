from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_ollama import ChatOllama

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------------------------------------------

# Instancias um chatmodel para comunicarmos com os modelos LLMs
model = ChatOllama(
    base_url="http://localhost:11434",
    model = "deepseek-r1",
    temperature = 0.2,
    num_predict = 1000, # mesmo funcionamento do max token
)

# --------------------------------------------------------------------------------------------------------------
## Definindo a estrutura da chain que vai avaliar a entrada e retornar uma classificação para nossa função 'executa_roteamento'
# Definindo a minha estrutura de saída usando Pydantic
class Rota(BaseModel):
    opcao: int = Field(description="Defina 1 se o usuário quiser criar um post do twitter e 2 se for um post do linkedin.")
    pergunta_user: str = Field(description="Colocar neste parametro a entrada do usuário sem alterá-la.")


parser = PydanticOutputParser(pydantic_object=Rota)

sys_prompt_rota = """Você é um especialista em classificação. Você receberá perguntas do usuário e precisará classificar, \
entre as opções 1 ou 2, se o usuário está solicitando um post para o twitter ou um post para o linkedin.
\n{format_instructions}\n
Entrada Usuário: {pergunta_user}"
"""

rota_prompt_template = ChatPromptTemplate([("system", sys_prompt_rota),],
                                          partial_variables={"format_instructions": parser.get_format_instructions()}
                                          )

# criando o pedaço da chain que controla o roteamento entre as branches
chain_de_roteamento = rota_prompt_template | model | parser

# --------------------------------------------------------------------------------------------------------------

# Definindo o prompt de criação de post twitter:

sys_twitter_prompt = """Você é um assistente especialista em criar conteúdo para o twitter e tem como objetivo \
criar os melhores tweets virais sobre o tema que o usuário te passar. Seja criativo e atenda ao padrão de 280 caracteres do \
twitter. RESPONDA EM PORTUGUÊS.
Entrada do usuário: {pergunta_user}
"""

prompt_template_twitter = ChatPromptTemplate([("system", sys_twitter_prompt),])

chain_twitter = prompt_template_twitter | model | StrOutputParser()

# --------------------------------------------------------------------------------------------------------------

# Definindo o prompt de criação de post linkedin:

sys_linkedin_prompt = """Você é um assistente especialista em criar conteúdo para o Linkedin e tem como objetivo \
criar os melhores posts profissionais e virais sobre o tema que o usuário te passar. Seja criativo. RESPONDA EM PORTUGUÊS.
Entrada do usuário: {pergunta_user}
"""

prompt_template_linkedin = ChatPromptTemplate([("system", sys_linkedin_prompt),])

chain_linkedin = prompt_template_linkedin | model | StrOutputParser()


## Definindo a função de escolha de roteamento (nó de rota)
def executa_roteamento(entrada: Rota):
    if entrada.opcao == 1:
        print(f"Opção classe Pydantic: {entrada.opcao} (Twitter)")
        return RunnableLambda(lambda x: {"pergunta_user": x.pergunta_user}) | chain_twitter
    else:
        print(f"Opção classe Pydantic: {entrada.opcao} (Linkedin)")
        return   RunnableLambda(lambda x: {"pergunta_user": x.pergunta_user}) | chain_linkedin

# --------------------------------------------------------------------------------------------------------------

# Crie a cadeia final usando LangChain Expression Language (LCEL)
chain = chain_de_roteamento | RunnableLambda(executa_roteamento)

# --------------------------------------------------------------------------------------------------------------

# Executando nossa chain principal.
# result = chain.invoke({"pergunta_user": "Crie 1 post do twitter sobre tecnologia"})

result = chain.invoke({"pergunta_user": "Crie 1 post do linkedin sobre tecnologia"})

# --------------------------------------------------------------------------------------------------------------
# Imprimindo a saida.
print("---------------")
print(result)
print("---------------")