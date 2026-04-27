# Fonte usada como exemplo FAQ da empresa Booking: https://www.booking.com/tpi_faq.pt-br.html
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

from dotenv import load_dotenv
load_dotenv()  # Carregando QDRANT_API_KEY e QDRANT_URL

# Definindo o modelo de embedding
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

NOME_COLECAO="FAQ_BOOKING"

# Função: Divide o documento em partes menores (chunks) de tamanho 1000 caracteres
def divide_texto(lista_documento_entrada):
    print(f">>> REALIZANDO A DIVISAO DO TEXTO ORIGINAL EM CHUNKS")
    text_splitter = RecursiveCharacterTextSplitter(separators=[""],  chunk_size=1000, chunk_overlap=200)
    # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200) # Caso queira usar o TXT
    documents = text_splitter.split_documents(lista_documento_entrada)
    return documents


# Cria o banco de dados vetorial, gerando os embeddings dos documentos
def cria_banco_vetorial_e_indexa_documentos(documentos):
    print(f">>> REALIZANDO INDEXAÇÃO DOS CHUNKS NO BANCO VETORIAL")
    QdrantVectorStore.from_documents(
        documents=documentos,
        embedding=embeddings_model,
        api_key=os.environ.get("QDRANT_API_KEY"),
        url=os.environ.get("QDRANT_URL"),
        prefer_grpc=True,
        collection_name=NOME_COLECAO
    )


# Função para carregar o texto de um arquivo e retornar como lista de documentos
def ler_txt_e_retorna_texto_em_document():
    print(f">>> REALIZANDO A LEITURA DO PDF EXEMPLO")
    lista_documentos = PyPDFLoader('FAQ_BOOKING_COM.pdf').load()
    # lista_documentos = TextLoader('FAQ_BOOKING_COM.txt', encoding='utf-8').load() # Caso queira usar o TXT
    return lista_documentos



texto_completo_lido = ler_txt_e_retorna_texto_em_document()
divide_texto_resultado = divide_texto(texto_completo_lido)
cria_banco_vetorial_e_indexa_documentos(divide_texto_resultado)
