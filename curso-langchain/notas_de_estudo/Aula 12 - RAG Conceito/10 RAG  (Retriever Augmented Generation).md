# Conceito de RAG

RAG (Retriever Augmented Generation) ou Geração aumentada via Recuperação corresponde ao processo de otimizar a saída de um grande modelo de linguagem, de forma que ele faça referência a uma base de conhecimento confiável fora das suas fontes de dados de treinamento antes de gerar uma resposta. A vantagem disso é evitar as possíveis **alucinações** e entregar informações que não fazem parte da base de conhecimento do LLM.  

Grandes modelos de linguagem (LLMs) são treinados em grandes volumes de dados e usam bilhões de parâmetros para gerar resultados originais para tarefas como responder a perguntas, traduzir idiomas e concluir frases. A RAG estende os já poderosos recursos dos LLMs para domínios específicos ou para a base de conhecimento interna de uma organização sem a necessidade de treinar novamente o modelo. É uma abordagem econômica para especializar o modelo em um contexto especifico.

**Problemas que RAG resolve:**
- Alucinação: entregar um contexto para o modelo LLM evita que ele crie informações incorretas com confiança. 
- Corte de conhecimento: os modelos eles são treinados com uma base de informações textuais até uma determinada data de corte, ou seja, conhecimentos gerados depois da data de corte não fará parte do conhecimento do modelo.
- Diminui o custo com tokens de entrada (evita enviar muitas informações desnecessárias no prompt de entrada, pois você passa a enviar as informações apenas mais similares à pergunta).
- Mais barato que fine-tuning.

Exemplo: 
Imagine que você está conversando com um assistente virtual. Você pergunta:  
**"Qual é a capital da Islândia?"**

Se o assistente **não tiver acesso a informações externas**, ele pode inventar algo, como:  
**"A capital da Islândia é Aurora."**  
Aqui, ele "alucinou", porque não tinha como saber a resposta correta e chutou.

Agora, imagine que o assistente tenha acesso a um livro de geografia. Antes de responder, ele vai até o livro, procura pela Islândia e encontra a resposta:  
**"A capital da Islândia é Reykjavík."**  
Aqui, o assistente usou o livro para buscar a informação e deu uma resposta correta com base no contexto que encontrou.

**Isso é RAG!**  
É uma forma de melhorar as respostas de um modelo de IA combinando duas etapas:

1. **Buscar informações em uma base externa (retrieval)**, como um documento ou uma base de dados.
2. **Gerar uma resposta usando essas informações (generation)**.

# Como funciona?

Explicação no board excalidraw