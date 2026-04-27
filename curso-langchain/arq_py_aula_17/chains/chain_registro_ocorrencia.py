from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os
import csv
from operator import itemgetter

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnableParallel

# Carregar as chaves APIs presentes no arquivo .env
load_dotenv()
# --------------------------------------------------------------------------------

# Instanciar um chatmodel para comunicarmos com os modelos LLMs
model_registro = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --------------------------------------------------------------------------------
# Criando o estruturador de saida:
class RegistroOcorrencia(BaseModel):
    nome: str = Field(description="Nome do usuário, se não tiver deixe vazio ('')")
    idade: str = Field(description="idade do usuário, se não tiver deixe vazio ('')")
    valido: bool = Field(description="Somente responda com True se você ter o nome e a idade do usuário, se não atribua False.")

# Criando o parser estruturado
parser_cadastro = PydanticOutputParser(pydantic_object=RegistroOcorrencia)


# Criando o ChatPromptTemplate que solicitará ao LLM que ele classifique a entrada do usuário:
sys_prompt_cadastro = """Você é responsável por cadastrar as informações do usuário em um banco quando o usuário \
desejar registrar uma ocorrência de Dengue. Para realizar o cadastro, você precisa conhecer o nome e idade do \
usuário caso desconheça, solicite. Não invente! Use as informações do histórico se te ajudar.

# Responda com essa estrutura:
\n{format_instructions}\n

Mensagem Usuário: {pergunta_usuario}"

## Histórico da conversa:

{history}
"""

cadastro_template = ChatPromptTemplate([("system", sys_prompt_cadastro),],
                                          partial_variables={"format_instructions": parser_cadastro.get_format_instructions()}
                                          )

def cadastro_dengue(entrada):
    arquivo_existe = os.path.isfile("../cadastro_dengue.csv")
    print(f">>>>> Entrada: {entrada}")
    if entrada.valido:
        with open("../cadastro_dengue.csv", mode="a", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            # Se for a primeira vez que escreve, adiciona o cabeçalho
            if not arquivo_existe:
                escritor.writerow(["nome", "idade"])
            # Escreve os dados no CSV
            escritor.writerow([entrada.nome, entrada.idade])

        return f"Cadastro da ocorrência realizada com sucesso."
    else:
        return f"Para que seja possível o cadastro da ocorrência, preciso do seu nome e idade! Poderia me passar por favor? O que tenho até agora > nome: {entrada.nome} | Idade {entrada.idade}"

# ----------------------------------------------------------------------------------------------------------------------

# Chain de finalização:
model_finalizacao = ChatOpenAI(model="gpt-4o", temperature=0.2)

# Criando o ChatPromptTemplate que vai finalizar a conversa dizendo oq ue está faltando ou se teve sucesso no cadastro da ocorrencia.
sys_prompt_finalizacao = """\
Você precisa informar ao usuário que está registrando uma ocorrência de Dengue se você conseguiu realizar o cadastro ou \
precisa de mais alguma informação. Use a resposta/observação que você recebeu do sistema para orientá-lo.

# Resposta do sistema de cadastro:
{acao_executada}
"""

# Criando o ChatPromptTemplate prompt de sistema e o histórico:
chat_prompt_finalizacao = ChatPromptTemplate([("system", sys_prompt_finalizacao),
                                               MessagesPlaceholder(variable_name="history"),
                                              ("human", "## Pergunta do Usuário: {pergunta_usuario}")

                                               ])


# ----------------------------------------------------------------------------------------------------------------------

# Criando a Chain que vai classificar a entrada do usuário e finalizar a operacao - Rota 3:
chain_de_cadastro = (RunnableParallel(
                    {"acao_executada": cadastro_template | model_registro | parser_cadastro | RunnableLambda(cadastro_dengue),
                     "history": itemgetter("history"),
                     "pergunta_usuario": itemgetter("pergunta_usuario")
                     })
                     | chat_prompt_finalizacao
                     | model_finalizacao
                     | StrOutputParser())









