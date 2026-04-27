from operator import itemgetter

from arq_py_aula_17.memorias.memoria_assinc import get_session_history, trimmer
from arq_py_aula_17.chains.chain_geral import chain_temas_nao_relacionados
from arq_py_aula_17.chains.chain_classifica import chain_de_roteamento
from arq_py_aula_17.chains.chain_rag_duvidas import chain_orientador
from arq_py_aula_17.chains.chain_registro_ocorrencia import chain_de_cadastro

from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory

# Necessário para trabalhar com o LangServer. Ele envia um input como mensagem ao invés de dict
def extract_query(input_data):
    # Se for uma lista (como em conversas com histórico), pega a última mensagem humana
    if isinstance(input_data, list):
        return input_data[-1].content
    # Se for um objeto de mensagem (como no LangServe)
    elif hasattr(input_data, 'content'):
        return input_data.content
    # Se já for string
    return input_data

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
chain_principal = (RunnableParallel({"input": itemgetter("input") | RunnableLambda(extract_query) ,
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
