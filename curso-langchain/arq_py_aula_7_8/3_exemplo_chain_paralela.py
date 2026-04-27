from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_openai import ChatOpenAI

# Carregar as chas APIs presentes no arquivo .env
load_dotenv()

# --------------------------------------------------------------------------------------------------------------

# Instancias um chatmodel para comunicarmos com os modelos LLMs
model = ChatOpenAI(model="gpt-4o", temperature=0.2)

# Definindo o prompt de comunicação - adotamos aqui um estilo chat prompt
# template, uma vez que estamos usando o modelo do tipo chat.

prompt_template_inicial = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um escritor especialista em análises de review de filmes de cinema."),
        ("human", "Liste de forma estruturada os principais detalhes e pontos de vistas apresentados na seguinte \
review entregue pelo usuário não invente nada apenas capture as principais informações apresentadas.\
Review: {movie_review}."),
    ]
)

# --------------------------------------------------------------------------------------------------------------

# Vamos definir um braço da nossa chain que será uma cadeia intermediária de analise dos pontos positivos sobre a review.

analise_ponto_positivo_template = ChatPromptTemplate(
    [
        ("system", "Você é um analista crítico de filmes de cinema"),
        (
            "human", "Dado este review estruturado: {review_estruturado}, liste os pontos positivos do filme.",
        ),
    ]
)


# criando a chain do braço 1
chain_intermediaria_positiva = analise_ponto_positivo_template | model | StrOutputParser()

# --------------------------------------------------------------------------------------------------------------

# Vamos definir outro braço da nossa chain que será uma cadeia intermediária de analise dos pontos negativos sobre a review.

analise_ponto_negativo_template = ChatPromptTemplate(
    [
        ("system", "Você é um analista crítico de filmes de cinema"),
        (
            "human", "Dado este review estruturado: {review_estruturado}, liste os pontos negativos do filme.",
        ),
    ]
)

# criando a chain do braço 2
chain_intermediaria_negativa = analise_ponto_negativo_template | model | StrOutputParser()

# --------------------------------------------------------------------------------------------------------------

# Função responsável por combinar os resultados dos braços que vão ser executados em paralelo.
def combinando_analises(entrada: dict):
    return f"Análise positiva:\n{entrada['posivita']}\n\nAnálise negativa:\n{entrada['negativa']}"
# --------------------------------------------------------------------------------------------------------------

# Crie a cadeia combinada usando LangChain Expression Language (LCEL)
# Em RunnableLambda(lambda x: {"review_estruturado": x}) estamos convertendo a saida string para um dicionário
# com a chave 'review_estruturado' que os templates das chains intermediárias exige como entrada.

chain = (prompt_template_inicial
         | model
         | StrOutputParser()
         | RunnableLambda(lambda x: {"review_estruturado": x}) # {"review_estruturado": x}
         | {"posivita": chain_intermediaria_positiva, "negativa": chain_intermediaria_negativa} # execução paralela
         | RunnableLambda(combinando_analises)
         )

# --------------------------------------------------------------------------------------------------------------

# Executando nossa chain principal.
movie_review ="""Crítica de "O Gladiador 2"
"O Gladiador 2", dirigido por Ridley Scott, chega aos cinemas com a expectativa de reviver a grandiosidade épica de \
seu antecessor. No entanto, apesar do histórico impressionante de Scott, que inclui clássicos como "Blade Runner" e \
"Alien", o filme parece tropeçar em sua própria ambição.

Desde o início, o filme tenta inovar ao incorporar cenas animadas e elementos de inteligência artificial, \
possivelmente como uma homenagem ao primeiro "Gladiador". No entanto, essa escolha estética, embora ousada, \
não se integra de maneira fluida à narrativa, criando uma desconexão que pode confundir o espectador.

A tentativa de trazer novidade às lutas no Coliseu, com a introdução de navios vikings e tubarões, é um exemplo \
de como o filme busca surpreender. No entanto, essas cenas acabam por sacrificar a autenticidade histórica em prol \
do espetáculo, o que pode afastar aqueles que esperavam uma representação mais fiel das arenas romanas. A inclusão \
de macacos em combate, por sua vez, remete a outras franquias cinematográficas, diluindo ainda mais a originalidade \
do enredo.

Apesar dessas escolhas questionáveis, é importante reconhecer o esforço de Scott em tentar oferecer algo novo e \
visualmente impactante. No entanto, a falta de uma pesquisa histórica mais aprofundada se faz sentir, e o filme \
poderia ter se beneficiado de uma abordagem mais cuidadosa nesse aspecto.

Em suma, "O Gladiador 2" é uma obra que, embora repleta de potencial e com momentos de brilho visual, acaba por se \
perder em sua tentativa de inovar. Para os fãs do gênero e do diretor, pode ser uma experiência mista, que levanta \
questões sobre até que ponto a inovação deve ir sem comprometer a essência e a coerência da narrativa.
"""

result = chain.invoke({"movie_review": movie_review})

# --------------------------------------------------------------------------------------------------------------
# Imprimindo a saida.
print(result)