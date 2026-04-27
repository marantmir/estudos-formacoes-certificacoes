from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda

# Carregar as chas APIs presentes no arquivo .env
load_dotenv()

# --------------------------------------------------------------------------------------------------------------

# Instancias um chatmodel para comunicarmos com os modelos LLMs
model = ChatOpenAI(model="gpt-4o", temperature=0.5)

# --------------------------------------------------------------------------------------------------------------
# Criando uma função personalizada para tratar a saida textual do LLM

def separador_de_tweet(entrada: str) -> list:
    """
    Função que recebe uma string e retorna uma lista com os elementos separados por quebras de linha.

    Args:
        entrada (str): A string de entrada, onde os valores estão separados por quebras de linha.

    Returns:
        list: Uma lista contendo cada elemento da string como um item separado.
    """
    # Divide a string em uma lista utilizando o caractere de quebra de linha '\n'
    elementos = entrada.split('\n')

    # Remove espaços extras e ignora linhas vazias
    elementos_limpos = [elemento.strip() for elemento in elementos if elemento.strip()]

    return elementos_limpos

# Criando uma função personalizada pegar a lista criada na função anterior e gerar um dicionário com o relátorio de
# analise de caracteres.

def relatorio_de_analise_de_caracteres(entrada: list) -> dict:
    """
    Função que gera um relatório com os tweets e a contagem de caracteres de cada tweet.

    Args:
        entrada (list): Lista de strings representando os tweets.

    Returns:
        dict: Um dicionário com duas chaves:
              - 'tweets': contendo a lista original.
              - 'num_caract': contendo uma lista com o número de caracteres de cada tweet.
    """
    # Gera a contagem de caracteres para cada item na lista
    contagem_caracteres = [len(tweet) for tweet in entrada]

    # Monta o dicionário de saída
    relatorio = {
        'tweets': entrada,
        'num_caract': contagem_caracteres
    }

    return relatorio

# --------------------------------------------------------------------------------------------------------------

# Definindo o prompt de comunicação - adotamos aqui um estilo chat prompt
# template, uma vez que estamos usando o modelo do tipo chat.

prompt_sistema = """Você é um assistente especialista em criar conteúdo para o twitter e tem como objetivo \
criar os melhores tweets virais sobre o tema que o usuário te passar. Seja criativo e atenda ao padrão de 280 caracteres do \
twitter.
Orientação:
- Crie apenas o numero de tweets informado.
- Separe cada um deles por uma quebra de linha,
"""

prompt_template = ChatPromptTemplate(
    [
        ("system", prompt_sistema),
        ("human", "Crie um total de {numero_de_publicacoes} tweets sobre o tema {input_tema}."),
    ])

# --------------------------------------------------------------------------------------------------------------


# Crie a cadeia combinada usando LangChain Expression Language (LCEL).
# para adicionar os outros componentes personalizados à cadeia, precisamos converter as funções em um componente langchain, para isso
# precisamos usar o RunnableLambda.

chain = prompt_template | model | StrOutputParser() | RunnableLambda(separador_de_tweet) | RunnableLambda(relatorio_de_analise_de_caracteres)

# --------------------------------------------------------------------------------------------------------------

# Executamos nossa chain
result = chain.invoke({"numero_de_publicacoes": 3, "input_tema": "tecnologia"})

# Imprimimos o nosso dicionário de relatório:
print(result)
print("-"*50)

# Imprimindo a saida de forma mais estruturada:
for i, (tweet, num_caract) in enumerate(zip(result['tweets'], result['num_caract']), start=1):
        print(f"Tweet {i}: {tweet}")
        print(f"Total de caracteres: {num_caract}")
        if num_caract <= 280:
            print("Validação: OK")
        else:
            print("Validação: Tweet supera o limite de 280 caracteres")
        print("-"*50)