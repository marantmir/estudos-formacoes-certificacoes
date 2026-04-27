# Fonte usada como exemplo FAQ da empresa Booking: https://www.booking.com/tpi_faq.pt-br.html
import os
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from typing import List
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()  # Carregando QDRANT_API_KEY e QDRANT_URL

# Definindo o modelo de embedding
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

NOME_COLECAO="FAQ_BOOKING"

# ---------------------- ATENÇÃO -------------------
# Antes de executar esse script é importante que você já tenha realizado a indexação das informações no seu
# banco vetorial. Você pode realizar o mesmo processo presente em 'arq_auxiliar_indexacao.py'.
# Aqui, estamos reaproveitando as informações já indexadas no exemplo anterior.
# --------------------------------------------------

# Conecta-se ao banco vetorial já existente
db = QdrantVectorStore.from_existing_collection(
        collection_name=NOME_COLECAO,
        url=os.environ.get("QDRANT_URL"),
        embedding=embeddings_model,
        api_key=os.environ.get("QDRANT_API_KEY")
    )

# Instancia o modelo LLM que vai executar a chain intermediária criando 3 perguntas semelhantes para realizar a indexação:
llm = ChatOpenAI(temperature=0)

# Cria o banco vetorial como recuperador:
db_retriever = db.as_retriever()

# A chain intermediária por padrão sem personalização vai criar 3 frases semelhantes à entrada passada antes de
# fazer o retrivever:
retriever_from_llm = MultiQueryRetriever.from_llm(retriever=db_retriever, llm=llm)

# Exemplo de consulta no banco:
# query = "Cancelaram minha reserva o que fazer?"
query = "Quando eu chego na hospedagem preciso pagar algo?"

# Executando o recuperador:
pedacos_retornados = db_retriever.invoke(query)


print(f"Total de pedaços retornados (documents): {len(pedacos_retornados)}\n")

for i, pedaco in enumerate(pedacos_retornados):
    print(f"------ (documents) chunk {i} -------")
    print(pedaco.page_content)
    print("-------------------------------------")


# # ----------------------------------------------------- VERSAO 2: ------------------------------------------------------
# # Caso você deseja personalizar o número de perguntas que são criadas no MultiQueryRetriever,
# # você pode criar uma chain separada e passar como parametro:
#
#
# # Criando o output parser (separando quebras de linha):
# class LineListOutputParser(BaseOutputParser[List[str]]):
#     """Output parser for a list of lines."""
#
#     def parse(self, text: str) -> List[str]:
#         lines = text.strip().split("\n")
#         return list(filter(None, lines))  # Remove empty lines
#
#
# output_parser = LineListOutputParser()
#
# # Criando o prompt que vai gerar as N perguntas semelhantes:
# QUERY_PROMPT = PromptTemplate(
#     input_variables=["question"],
#     template="""Você é um assistente de modelo de linguagem de IA. Sua tarefa é gerar cinco \
# diferentes versões da pergunta do usuário para recuperar documentos relevantes de um vetor \
# banco de dados. Ao gerar múltiplas perspectivas sobre a pergunta do usuário, seu objetivo é ajudar\
# o usuário supera algumas das limitações da busca por similaridade baseada em distância.
# Forneça essas perguntas alternativas separadas por novas linhas.
# Pergunta original: {question}""")
#
#
# # Chain
# llm_chain = QUERY_PROMPT | llm | output_parser
#
#
#
# # Cria o recuperador
# retriever = MultiQueryRetriever(retriever=db_retriever, llm_chain=llm_chain, parser_key="lines")
#
# # Executar o recuperador:
# # query = "Cancelaram minha reserva o que fazer?"
# query = "Quando eu chego na hospedagem preciso pagar algo?"
# pedacos_retornados = retriever.invoke(query)
#
# print(f"Total de pedaços retornados (documents): {len(pedacos_retornados)}\n")
#
# for i, pedaco in enumerate(pedacos_retornados):
#     print(f"------ (documents) chunk {i} -------")
#     print(pedaco.page_content)
#     print("-------------------------------------")