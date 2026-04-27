from operator import itemgetter

from arq_py_aula_17.memorias.memoria import get_session_history, trimmer
from arq_py_aula_17.chains.chain_geral import chain_temas_nao_relacionados
from arq_py_aula_17.chains.chain_classifica import chain_de_roteamento
from arq_py_aula_17.chains.chain_rag_duvidas import chain_orientador
from arq_py_aula_17.chains.chain_registro_ocorrencia import chain_de_cadastro

from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory


## Definindo a função de escolha de roteamento (nó que irá classificar a pergunta do usuário e mandar para o `braço` correspondente do fluxo):
# Rota 1 - Usuário desejando informações sobre a Dengue com base em RAG
# Rota 2 - Usuário perguntando sobre temas gerais ou dando uma saudação.
# Rota 3 - Usuário desejando cadastrar que está com Dengue.

def executa_roteamento(entrada: dict):
    if entrada["resposta_pydantic"].opcao == 1:
        print(f">> Opção classe Pydantic: {entrada['resposta_pydantic'].opcao} (Informações sobre Dengue)")
        return RunnableLambda(lambda x: {"pergunta_usuario": x['input'], "history": x['history']}) | chain_orientador
    elif entrada["resposta_pydantic"].opcao == 2:
        print(f">> Opção classe Pydantic: {entrada['resposta_pydantic'].opcao} (Assuntos Gerais e Saudações)")
        return RunnableLambda(lambda x: {"pergunta_usuario": x['input'], "history": x['history']}) | chain_temas_nao_relacionados
    elif entrada["resposta_pydantic"].opcao == 3:
        print(f">> Opção classe Pydantic: {entrada['resposta_pydantic'].opcao} (Cadastro de ocorrência Dengue!)")
        return RunnableLambda(lambda x: {"pergunta_usuario": x['input'], "history": x['history']}) | chain_de_cadastro
    else:
        print("Opção escolhida pelo LLM não maepada.")



# Crie a cadeia final usando LangChain Expression Language (LCEL)
chain_principal = (RunnableParallel({"input": itemgetter("input"),
                                     "history": itemgetter("history"),
                                     "resposta_pydantic": chain_de_roteamento
                                     })
                   | RunnableLambda(executa_roteamento))



## Encapsulando nossa chain com a classe de gestão de mensagens de histórico
chain_principal_com_trimming = (
    RunnablePassthrough.assign(history=itemgetter("history") | trimmer)
    | chain_principal
)

runnable_with_history = RunnableWithMessageHistory(
    chain_principal_com_trimming,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# ATENÇÃO: ANTES DE EXECUTAR É IMPORTANTE REALIZAR A INDEXAÇÃO DAS INFORMAÇÕES NO
# BANCO VETORIAL. CONSULTAR O ARQUIVO 'indexacao_informacao.py'.
# --------------------------------------------------------------------------------

def menu():
    session_id = 1
    while True:
        print("\nOpções:")
        print("q -> Sair")
        print("1 -> Continuar conversa no mesmo Chatbot")
        print("2 -> Abrir um novo Chat")
        opcao = input("Escolha uma opção: ").strip().lower()

        if opcao == 'q':
            print("Saindo do programa...")
            break
        elif opcao == '1':
            query = input("Digite aqui sua mensagem: ")
            result = runnable_with_history.invoke(
                {"input": query},
                config={"configurable": {"session_id": session_id}},
            )
            print("---------- RESPOSTA LLM ----------")
            print(f"\033[1;32m{result}\033[0m")
            print("----------------------- ----------")
        elif opcao == '2':
            session_id += 1
            query = input("Digite aqui sua mensagem: ")
            result = runnable_with_history.invoke(
                {"input": query},
                config={"configurable": {"session_id": session_id}},
            )
            print("---------- RESPOSTA LLM ----------")
            print(f"\033[1;32m{result}\033[0m")
            print("----------------------- ----------")
        else:
            print("Opção inválida. Tente novamente.")

# Executa o menu
menu()