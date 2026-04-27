from langchain_community.document_loaders import TextLoader

loader = TextLoader(r"D:\AulasYoutube\LangChainCourse\curso-langchain\arq_py_aula_9\exemplo_arquivo.txt") # mudar aqui para o caminho do seu computador
pages_sinc = loader.load()

# Aqui verificaremos que pages_sinc é uma lista de 'Document':
print("\n------ Imprimindo o resultado ------\n")
print(pages_sinc)

print("\n------ Imprimindo o resultado ------\n")
# Acessando os valores carregados:
for elemento in pages_sinc:
    print("----- Página Inicio -----")
    print(f"Conteúdo: {elemento.page_content}\n")
    print(f"Metadado: {elemento.metadata}")
    print("----- Página Fim    -----")

