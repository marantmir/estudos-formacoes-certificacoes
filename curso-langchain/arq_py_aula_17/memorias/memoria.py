from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.messages import trim_messages


## Criando o gestor de memória (histórico): Função para retornar o histórico de mensagens com base no `session_id`

def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, connection="sqlite:///memorychatbot.db")

# Criando a função que corta o histórico e captura as 10 ultimas mensagens trocadas na conversa:
trimmer = trim_messages(strategy="last", max_tokens=10, token_counter=len)

