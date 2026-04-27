## Documentacao
# https://python.langchain.com/docs/how_to/#prompt-templates

# Parte 1 - Importando os componentes do LangChain
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage

# Parte 2 - Pratica
# ========= Exemplo 1 =============

print("=========== Exemplo 1 =========")
prompt_template = PromptTemplate.from_template("Gere para mim um poema sobre: {assunto}. Escreva em {lingua}")
retorno = prompt_template.invoke({"assunto": "navegação", "lingua":"pt-br"})

print(retorno)

# ========= Exemplo 2 =============

print("=========== Exemplo 2 =========")

prompt_template = ChatPromptTemplate(
    ["Gere para mim um poema sobre: {assunto}. Escreva em {lingua}"
     ]
)

retorno = prompt_template.invoke({"assunto": "navegação", "lingua":"pt-br"})
print(retorno)

# ========= Exemplo 2 Alternativos =============

print("=========== Exemplo 2 - Alternativa 1 =========")


prompt_template = ChatPromptTemplate(
    [
        HumanMessagePromptTemplate.from_template("Gere para mim um poema sobre: {assunto}. Escreva em {lingua}")
    ]
)

retorno = prompt_template.invoke({"assunto": "navegação", "lingua":"pt-br"})
print(retorno)

print("=========== Exemplo 2 - Alternativa 2 =========")

prompt_template = ChatPromptTemplate(
    [
        ("user", "Gere para mim um poema sobre: {assunto}. Escreva em {lingua}")
     ])

retorno = prompt_template.invoke({"assunto": "navegação", "lingua":"pt-br"})
print(retorno)

# ========= Exemplo 3 =============
print("=========== Exemplo 3 =========")

prompt_template = ChatPromptTemplate([
									  ("system", "Você é um assistente de IA com habilidade de escritor de poesia."),
									  ("user", "Gere para mim um poema sobre: {assunto}. Escreva em {lingua}")
])

retorno = prompt_template.invoke({"assunto": "navegação", "lingua":"pt-br"})
print(retorno)

# ========= Exemplo 3 Alternativo =============
print("=========== Exemplo 3 - Alternativa 1 =========")


prompt_template = ChatPromptTemplate([
    ("system", "Você é um assistente de IA com habilidade de escritor de poesia."),
	MessagesPlaceholder("msgs_user")
]
)

retorno = prompt_template.invoke(
    {"msgs_user": [HumanMessage(content="Gere para mim um poema sobre: navegação. Escreva em pt-br")]
     })
print(retorno)