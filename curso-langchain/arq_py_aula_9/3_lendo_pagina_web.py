from langchain_community.document_loaders import WebBaseLoader

page_url = "https://python.langchain.com/docs/introduction/"

loader = WebBaseLoader(web_paths=[page_url])
resultado = loader.load()


# Aqui verificaremos que pages_sinc é uma lista de 'Document':
print("\n------ Imprimindo o resultado ------\n")
print(resultado)

print("\n------ Imprimindo o resultado ------\n")
# Acessando os valores carregados:
for elemento in resultado:
    print("----- Página Inicio -----")
    print(f"Conteúdo: {elemento.page_content}\n")
    print(f"Metadado: {elemento.metadata}")
    print("----- Página Fim    -----")
