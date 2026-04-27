from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Carregar as chaves APIs presentes no arquivo .env
load_dotenv()
# --------------------------------------------------------------------------------

# Instanciar um chatmodel para comunicarmos com os modelos LLMs
model_classificador = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# --------------------------------------------------------------------------------
# Criando o classificador da pergunta de entrada do usuário:
class ClassificaEntrada(BaseModel):
    opcao: int = Field(description="Defina 1 se a pergunta do usuário solicitar informações ou orientações sobre Dengue ou gráfico da dengue. \
Defina 2  se for saudações ou temas que não são referentes à Dengue.\
Defina 3 se for uma solicitação de cadastro de ocorrência de Dengue ou se a pessoa está registrando que está com Dengue.")

# Criando o parser estruturado
parser_classifica = PydanticOutputParser(pydantic_object=ClassificaEntrada)


# Criando o ChatPromptTemplate que solicitará ao LLM que ele classifique a entrada do usuário:
sys_prompt_rota = """Você é um especialista em classificação. Você receberá perguntas do usuário e precisará classificá-las \
da melhor forma entre as opções estabelecidas.
Também preste atenção ao histórico da conversa quando você for realizar a classificação, pois durante um cadastro de \
ocorrência pode ser solicitado novas informações do usuário e a classificação pode ser com base no contexto histórico. 

\n{format_instructions}\n

Pergunta Usuário: {input}

## Historico da conversa:
{history}
"""

rota_prompt_template = ChatPromptTemplate([("system", sys_prompt_rota),],
                                          partial_variables={"format_instructions": parser_classifica.get_format_instructions()}
                                          )

# Criando a Chain que vai classificar a entrada do usuário:
chain_de_roteamento = rota_prompt_template | model_classificador | parser_classifica


