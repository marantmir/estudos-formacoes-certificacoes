from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field
# Carregar as chas APIs presentes no arquivo .env
load_dotenv()

# --------------------------------------------------------------------------------------------------------------

# Instancias um chatmodel para comunicarmos com os modelos LLMs
model = ChatOpenAI(model="gpt-4o", temperature=0.2)

# --------------------------------------------------------------------------------------------------------------
## Definindo a estrutura da chain que vai avaliar a entrada e retornar uma classificação para nossa função 'executa_roteamento'
# Definindo a minha estrutura de saída usando Pydantic
class Rota(BaseModel):
    opcao: bool = Field(description="Defina True se necessitar atendimento humano e false caso contrário.")
    pergunta_user: str = Field(description="Colocar neste parametro a pergunta do usuário sem alterá-la.")


parser = PydanticOutputParser(pydantic_object=Rota)

sys_prompt_rota = """Você é um especialista em classificação. Você receberá perguntas do usuário e precisará classificar, \
de forma booleana, se o usuário está solicitando conversar com um atendente humano ou não.
\n{format_instructions}\n
Pergunta Usuário: {pergunta_user}"
"""

rota_prompt_template = ChatPromptTemplate([("system", sys_prompt_rota),],
                                          partial_variables={"format_instructions": parser.get_format_instructions()}
                                          )

# criando o pedaço da chain que controla o roteamento entre as branches
chain_de_roteamento = rota_prompt_template | model | parser

# Se quiser testar a cadeia intermediária de roteamento:
# result = chain_de_roteamento.invoke({"pergunta_user": "Quero falar com um humano"})

# --------------------------------------------------------------------------------------------------------------

# Definindo o prompt de chatbot que tira duvidas do usuário:

sys_chatbot_prompt = """Você é um assistente de uma clinica odontológica e tem como objetivo responder à perguntas dos clientes. A seguir você \
encontra a FAQ do nosso site, use essas informações para realizar o atendimento e tirar dúvidas. Caso você desconheça alguma \
informação, não invente. Seja sempre amigável e esteja disposto a ajudar!

**FAQ - Clínica Odontológica**
1. **Quais serviços a clínica oferece?**  
   Oferecemos tratamentos como limpeza dental, clareamento, ortodontia, implantes, próteses, tratamento de canal e estética dental.
2. **A clínica aceita convênios?**  
   Sim, trabalhamos com os principais convênios odontológicos. Consulte nossa equipe para verificar se aceitamos o seu.
3. **Como agendar uma consulta?**  
   Você pode agendar sua consulta pelo telefone, WhatsApp ou diretamente em nosso site.
4. **Quanto tempo dura uma consulta?**  
   Depende do procedimento, mas consultas de rotina geralmente duram entre 30 e 60 minutos.
5. **Vocês atendem emergências?**  
   Sim, oferecemos atendimento emergencial para dores agudas, traumas ou casos de urgência.
6. **É possível parcelar tratamentos?**  
   Sim, oferecemos opções de parcelamento. Entre em contato para conhecer os detalhes.
7. **Crianças podem ser atendidas na clínica?**  
   Sim, contamos com profissionais especializados em odontopediatria para cuidar dos sorrisos dos pequenos.
8. **O clareamento dental é seguro?**  
   Sim, nossos tratamentos de clareamento são realizados com técnicas e produtos seguros, supervisionados por especialistas.
Se tiver mais dúvidas, entre em contato conosco! 😊

Dúvida do usuário: {pergunta_user}
"""

prompt_template_chatbot = ChatPromptTemplate([("system", sys_chatbot_prompt),])

chain_chatbot = prompt_template_chatbot | model | StrOutputParser()

## Definindo a função de escolha de roteamento (nó de rota)
def executa_roteamento(entrada: Rota):
    if entrada.opcao:
        print(f"Opção classe Pydantic: {entrada.opcao} (Atendimento humano)")
        return "Atendimento redirecionado para um humano. Favor aguardar alguns minutos que já vamos te atender!"
    else:
        print(f"Opção classe Pydantic: {entrada.opcao} (Atendimento Chatbot)")
        return   RunnableLambda(lambda x: {"pergunta_user": x.pergunta_user}) | chain_chatbot

# --------------------------------------------------------------------------------------------------------------

# Crie a cadeia final usando LangChain Expression Language (LCEL)
chain = chain_de_roteamento | RunnableLambda(executa_roteamento)

# --------------------------------------------------------------------------------------------------------------

# Executando nossa chain principal.
result = chain.invoke({"pergunta_user": "Quais serviços a clínica oferece?"})

# --------------------------------------------------------------------------------------------------------------
# Imprimindo a saida.
print("---------------")
print(result)
print("---------------")