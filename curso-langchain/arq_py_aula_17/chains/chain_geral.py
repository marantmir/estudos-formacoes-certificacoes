from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# Carregar as chaves APIs presentes no arquivo .env
load_dotenv()

# --------------------------------------------------------------------------------

# Instanciar um chatmodel para comunicarmos com os modelos LLMs
model_fora_do_tema = ChatOpenAI(model="gpt-4o", temperature=0.2)

# Criando o ChatPromptTemplate que vai agir como um personal para tirar dúvidas do usuário
sys_prompt_fora_do_tema = """Você é um assistente de saúde se o usuário fez uma saudação, responda \
de forma amigável e sugira o que você pode fazer como por exemplo responder sobre dúvidas a respeito da Dengue, \
dar orientações sobre as causas, tratamento e sintomas da Dengue ou registrar uma ocorrência de Dengue.
Se usuário fez uma pergunta não pertinente ao tema, informe que você não é capaz de \
responder sobre estes assuntos e que seu papel é tirar dúvidas sobre saúde."""

# Criando o ChatPromptTemplate com a entrada do usuário e o histórico:
fora_do_tema_prompt_template = ChatPromptTemplate([("system", sys_prompt_fora_do_tema),
                                               MessagesPlaceholder(variable_name="history"),
                                               ("human", "Dúvida do usuário: {pergunta_usuario}"),
                                               ])

# Criando a Chain que vai responder ao usuário - Rota 2:
chain_temas_nao_relacionados = fora_do_tema_prompt_template | model_fora_do_tema | StrOutputParser()

