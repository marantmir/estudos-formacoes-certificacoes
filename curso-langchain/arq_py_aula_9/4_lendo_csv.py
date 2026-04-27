from langchain_community.document_loaders.csv_loader import CSVLoader

file_path = r"D:\AulasYoutube\LangChainCourse\curso-langchain\arq_py_aula_9\exemplo_arquivo.csv"  # mudar aqui para o caminho do seu computador

loader = CSVLoader(file_path)
data = loader.load()

linha = 0
for record in data:
    print(f"Imprimindo linha: {linha}")
    print(f"-----------")
    print(record)
    print(f"-----------")
    linha+=1
print("---- Imprimindo de forma estruturada ----")
for record in data:
    print(f"Imprimindo linha: {linha}")
    print(f"Conteúdo: {record.page_content}\n")
    print(f"-----------")
    linha+=1
