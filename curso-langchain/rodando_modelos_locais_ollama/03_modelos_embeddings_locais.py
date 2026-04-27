from langchain_ollama import OllamaEmbeddings

embeddings_model = OllamaEmbeddings(model="nomic-embed-text")

documents = [
    "Olá!",
    "Quantos anos você tem?",
    "Qual seu nome?",
    "Meu amigo se chama flávio",
    "Oi!"
]

# Esta função é utilizada quando você tem uma lista de strings ao invés de documentos.
embeddings = embeddings_model.embed_documents(documents)

print("----- QUANTOS VETORES EXISTEM -----")        # Deve ser 5, pois temos 5 documentos
print(len(embeddings))        # Deve ser 5, pois temos 5 documentos
print("-----------------------------------------------------------------")

print("\n----- DIMENSÃO DOS VETORES -----")
print("O Modelo de embedding large da OpenIA, deve ter um tamanho de 3072.")
print(len(embeddings[0]))     # Cada embedding costuma ter 768 dimensões, dependendo do modelo
print("-----------------------------------------------------------------")

print("\n----- CONVERTENDO UMA PERGUNTA EM EMBEDDING -----")
embedded_query = embeddings_model.embed_query("Qual é o nome do seu amigo?")

print("\n----- DIMENSÃO DOS VETORES -----")
print("Como na query tmb utilizamos o mesmo modelo, a dimensão será igual dos documentos.")
print(len(embedded_query))  # Tamanho do vetor da query (ex. 768)

print("-----------------------------------------------------------------")
print("\n----- Imprimindo o vetor Numérico -----")
print(embedded_query)  # Tamanho do vetor da query (ex. 768)

