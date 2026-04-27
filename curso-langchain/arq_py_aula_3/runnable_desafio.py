from langchain_core.runnables import RunnableLambda, RunnablePassthrough, RunnableParallel

""" Desafio com Runnables:

Processo:

1) Receber a entrada do tipo {"input": "Parabéns Você"}  e passar para frente (testar uso do RunnablePassthrough)

2) Quando eu receber a entrada de (1) eu gostaria de criar um dicionário mantendo a entrada de (1) intacta, mas criando 
uma chave nova ("num_caract") tal que seja a entrada de (1) contando o total de caracteres.

3) Usando a saída de (2) quero paralelizar a entrada em dois processos, o primeiro, pegando a entrada textual e 
adicionando a palavra " Conseguiu!" numa chave chamada "transformar_entrada" o segundo não farei nada, apenas passarei 
para frente a entrada sem qualquer alteração numa chave "passa_para_frente".

4) Por fim, vou passar para frente a combinação do processo paralelo e imprimir o resultado.

"""

# Parte 1
parte_1_runnable = RunnablePassthrough()

# Parte 2
def conta_caracteres(entrada: dict) -> int:
    return len(entrada["input"])

convert_funcao = RunnableLambda(conta_caracteres)

parte_2_runnable = RunnablePassthrough.assign(num_caract=convert_funcao)

# Parte 3
def transforma(entrada: dict) -> str:
    resultado = entrada["input"] + " Conseguiu!"
    return resultado

parte_3_transforma_entrada = RunnableLambda(transforma)
parte_3_passa_para_frente = RunnablePassthrough()

parte_3_runnable = RunnableParallel({
    "transformar_entrada": parte_3_transforma_entrada,
    "passa_para_frente": parte_3_passa_para_frente
}
)

# Parte 4
parte_4_runnable = RunnablePassthrough()

# Unindo tudo:

chain = parte_1_runnable | parte_2_runnable | parte_3_runnable | parte_4_runnable

## Invocar:


resposta = chain.invoke({"input": "Parabéns Você"})

print("------ RESPOSTA DO DESAFIO -----------------------")
print(resposta)
print("--------------------------------------------------")

