import os
from dotenv import load_dotenv
from operator import itemgetter

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_qdrant import QdrantVectorStore
from langchain_core.runnables import RunnableParallel, RunnableLambda

# Carregar as chaves APIs presentes no arquivo .env
load_dotenv()

# --------------------------------------------------------------------------------

# Instanciar um chatmodel para comunicarmos com os modelos LLMs
model_atendimento_orientador = ChatOpenAI(model="gpt-4o", temperature=0.2)

# Instanciar modelo de Embedding
modelo_embedding = OpenAIEmbeddings(model="text-embedding-3-large")

# Banco Vetorial
db_vetorial = QdrantVectorStore.from_existing_collection(
        collection_name="chatbot_saude",
        url=os.environ.get("QDRANT_URL"),
        embedding=modelo_embedding,
        api_key=os.environ.get("QDRANT_API_KEY")
    )

db_retriever = db_vetorial.as_retriever(search_kwargs={'k': 5})

def cria_texto_dos_documentos_retornados(documentos):
    """Função para pegar o conteúdo de cada chunk e criar um unico texto/string"""
    print(f">> Recuperador executado! Veja os documentos retornados:{documentos}")
    for i in documentos:
        print("--------------------- chunk --------------------")
        print(i.page_content)
        print("------------------------------------------------")
    return "\n\n".join(doc.page_content for doc in documentos)

# Criando o ChatPromptTemplate que vai agir como um personal para tirar dúvidas do usuário

sys_rag_prompt = """\
## Seu Papel:
Você é um assistente de saúde e tem como objetivo responder à perguntas dos usuários. As perguntas serão sobre o tema da \
Dengue e você tem o objetivo de orientá-los.

## Regras:
1 - Nunca invente informação. Responda que desconhece o assunto se você não souber responder.
2 - Sempre se baseie no contexto que é entregue entre as tags <contexto></contexto>. As informações presentes nestas tags \
foram obtidas de uma base de conhecimento.
3 - Evite falar 'no contexto...' ou 'conforme o contexto...' porque o usuário desconheçe sobre a presença desse contexto.

## Contexto Recuperado:
<contexto>
{contexto_obtido}
</contexto>
"""

# Criando o ChatPromptTemplate com a entrada do usuário e o histórico:
prompt_template_orientador = ChatPromptTemplate([("system", sys_rag_prompt),
                                                  MessagesPlaceholder(variable_name="history"),
                                                  ("human", "## Pergunta do Usuário: {pergunta_usuario}"),
                                                  ])

# Criando a Chain que vai responder ao usuário - Rota 1:
# Lembrar que o que está chegando aqui como entrada é um dict pergunta_usuario e history e o retriever usa apenas "pergunta_usuario", por isso 'itemgetter'
chain_orientador = (RunnableParallel({"pergunta_usuario": itemgetter("pergunta_usuario"),
                                      "history": itemgetter("history"),
                                      "contexto_obtido": itemgetter("pergunta_usuario") | db_retriever | cria_texto_dos_documentos_retornados
                                      })
                                      | prompt_template_orientador
                                      | model_atendimento_orientador
                                      | StrOutputParser())

