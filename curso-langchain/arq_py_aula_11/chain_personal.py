from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# Carregar as chaves APIs presentes no arquivo .env
load_dotenv()

# --------------------------------------------------------------------------------

# Instanciar um chatmodel para comunicarmos com os modelos LLMs
model_personal = ChatOpenAI(model="gpt-4o", temperature=0.2)

# Criando o ChatPromptTemplate que vai agir como um personal para tirar dúvidas do usuário
sys_prompt_personal = """Você é um personal trainer renomado e entende de todos os tipos de treinos para todos os tipos de \
fisicos. VOcê precisa responder à dúvidas do usuário sobre exercicios ou treinos. Seja amigável e detalhista. Apoie sempre \
seu aluno.
"""

# Criando o ChatPromptTemplate com a entrada do usuário e o histórico:
personal_prompt_template = ChatPromptTemplate([("system", sys_prompt_personal),
                                               MessagesPlaceholder(variable_name="history"),
                                               ("human", "Dúvida do usuário: {input_user}"),
                                               ])

# Criando a Chain que vai classificar a entrada do usuário:
chain_personal = personal_prompt_template | model_personal | StrOutputParser()

