# Fonte usada como exemplo FAQ da empresa Booking: https://www.booking.com/tpi_faq.pt-br.html
import os
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

from dotenv import load_dotenv
load_dotenv()  # Carregando QDRANT_API_KEY e QDRANT_URL

# Definindo o modelo de embedding
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

NOME_COLECAO="FAQ_BOOKING"


# Conecta-se ao banco vetorial já existente
db = QdrantVectorStore.from_existing_collection(
        collection_name=NOME_COLECAO,
        url=os.environ.get("QDRANT_URL"),
        embedding=embeddings_model,
        api_key=os.environ.get("QDRANT_API_KEY")
    )


# Banco Vetorial como Recuperador:
# db_retriever = db.as_retriever()

# Banco Vetorial como Recuperador, configurando parâmetros:
# db_retriever = db.as_retriever(search_kwargs={'k': 5, })
db_retriever = db.as_retriever(search_type="mmr", search_kwargs={'k': 3, 'fetch_k': 10})



# Exemplo de consulta no banco:
query = "Cancelaram minha reserva o que fazer?"
# query = "Quando eu chego na hospedagem preciso pagar algo?"
pedacos_retornados = db_retriever.invoke(query)


print(f"Total de pedaços retornados (documents): {len(pedacos_retornados)}")

for i, pedaco in enumerate(pedacos_retornados):
    print(f"------ (documents) chunk {i} -------")
    print(pedaco.page_content)
    print("-------------------------------------")
