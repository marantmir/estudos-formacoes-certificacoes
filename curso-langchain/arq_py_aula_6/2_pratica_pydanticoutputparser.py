from dotenv import load_dotenv
load_dotenv()

# Realizando as importações:
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Prática 2 - PydanticOutputParser

# Definindo o modelo
model = ChatOpenAI(model="gpt-4o", temperature=0)


# Definindo a minha estrutura de saída usando Pydantic
class Rota(BaseModel):
    escolha: int = Field(description="Rota escolhida")
    pensamento: str = Field(description="Campo para o pensamento que levou a decisão da rota escolhida")


# Criando o analisador de saída
parser = PydanticOutputParser(pydantic_object=Rota)

# Enviando ao prompt, minha estrutura esperada de resposta.
prompt_template = ChatPromptTemplate([("system",
                                       "Se a pergunta do usuário for relacionado ao setor financeiro, \
                                       a escolha deve ser 1, caso contrário a escolha pode ser qualquer numero \
                                       diferente de 1. \n{format_instructions}\n Pergunta Usuário: {pergunta_user}")],
                                     partial_variables={"format_instructions": parser.get_format_instructions()})

# Criando a Chain
chain = prompt_template | model | parser

output = chain.invoke({"pergunta_user": "Me diga quanto está o dollar."})

print("--"*50)
print("Tipo da saida:")
print(type(output))
print("--"*50)
print("Saida estruturada:")
print(output)
print("--"*50)
print("Consigo acessar cada parametro da minha classe pydantic, veja:")
print(f"Valor do parametro 'escolha': {output.escolha}")
print(f"Valor do parametro 'pensamento': {output.pensamento}")
print("--"*50)

