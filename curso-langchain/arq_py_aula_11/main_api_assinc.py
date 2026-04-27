from chain_de_classificacao_e_roteamento import chain_de_roteamento
from chain_personal import chain_personal
from chain_atendimento_geral import chain_de_atendimento_geral
from chain_temas_nao_relacionados import chain_temas_nao_relacionados
# alterado aqui!
from memoria_sistema_assincrono import get_session_history, trimmer

from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.runnables.history import RunnableWithMessageHistory



## Definindo a função de escolha de roteamento (nó que irá classificar a pergunta do usuário e mandar para o `braço`
# correspondente do fluxo):
def executa_roteamento(entrada: dict):
    if entrada["resposta_pydantic"].opcao == 1:
        print(f">> Opção classe Pydantic: {entrada['resposta_pydantic'].opcao} (Atendimento Geral)")
        return RunnableLambda(lambda x: {"input_user": x['input'], "history": x['history']}) | chain_de_atendimento_geral
    elif entrada["resposta_pydantic"].opcao == 2:
        print(f">> Opção classe Pydantic: {entrada['resposta_pydantic'].opcao} (Atendimento realizado pelo personal)")
        return RunnableLambda(lambda x: {"input_user": x['input'], "history": x['history']}) | chain_personal
    else:
        print(f">> Opção classe Pydantic: {entrada['resposta_pydantic'].opcao} (Assuntos não relacionados à academia)")
        return RunnableLambda(lambda x: {"input_user": x['input'], "history": x['history']}) | chain_temas_nao_relacionados


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


## Vamos testar com
# Olá Tudo bem? Sou gustavo!
# Gostaria de saber sobre os planos que vocês possuem, pode me contar mais?
# Sou iniciante como poderia ser meu treino? Tenho 165 cm de altura e 95 kg.
# Você pode me ajusar com astrologia?
