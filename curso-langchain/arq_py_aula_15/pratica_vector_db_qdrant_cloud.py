import os
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

from dotenv import load_dotenv
load_dotenv()  # Carregando QDRANT_API_KEY e QDRANT_URL

# Definindo o modelo de embedding
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")


# Função: Divide o documento em partes menores (chunks) de tamanho 1000 caracteres
def divide_texto(lista_documento_entrada):
    print(f">>> REALIZANDO A DIVISAO DO TEXTO ORIGINAL EM CHUNKS")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    documents = text_splitter.split_documents(lista_documento_entrada)
    i = 0
    for pedaco in documents:
        print("--" * 30)
        print(f"Chunk: {i}")
        print("--" * 30)
        print(pedaco)
        print("--" * 30)
        i += 1
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
        collection_name="colecao_youtube"
    )


# Função para carregar o texto de um arquivo e retornar como lista de documentos
def ler_txt_e_retorna_texto_em_document():
    print(f">>> REALIZANDO A LEITURA DO TXT EXEMPLO")
    lista_documentos = TextLoader('exemplo_texto.txt', encoding='utf-8').load()
    print("Texto lido e convertido em Document")
    print(lista_documentos)
    print("-----------------------------------")
    return lista_documentos


# Conecta-se ao banco vetorial já existente
def conecta_banco_vetorial_pre_criado():
    server = QdrantVectorStore.from_existing_collection(
        collection_name="colecao_youtube",
        url=os.environ.get("QDRANT_URL"),
        embedding=embeddings_model,
        api_key=os.environ.get("QDRANT_API_KEY")
    )
    return server


# Menu de opções
def menu():
    while True:
        print("\nOpções:")
        print("q -> Sair")
        print("1 -> Indexar informações no banco")
        print("2 -> Apenas conectar ao banco existente")
        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == 'q':
            print("Saindo do programa...")
            break
        elif opcao == '1':
            # Processa a leitura, divisão e indexação do texto
            texto_completo_lido = ler_txt_e_retorna_texto_em_document()
            divide_texto_resultado = divide_texto(texto_completo_lido)
            cria_banco_vetorial_e_indexa_documentos(divide_texto_resultado)
            print("Indexação concluída!")
        elif opcao == '2':
            # Apenas conecta ao banco existente
            print("Conectando ao banco vetorial existente...")
            db = conecta_banco_vetorial_pre_criado()
            print("Conexão estabelecida com sucesso!")
            # Exemplo de consulta no banco:
            query = input("Digite uma consulta para teste: ")
            pedacos_retornados = db.similarity_search(query, k=2)
            print(f"Total de pedaços retornados: {len(pedacos_retornados)}")
            for i, pedaco in enumerate(pedacos_retornados):
                print(f"------ chunk {i} -------")
                print(pedaco.page_content)
                print("--------------------")
        else:
            print("Opção inválida. Tente novamente.")


# Executa o menu
menu()
