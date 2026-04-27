# https://python.langchain.com/docs/how_to/semantic-chunker/
from langchain_core.documents import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

# Carregando a chave de API da Open AI
from dotenv import load_dotenv
load_dotenv()

# Texto modelo:
text = """A inteligência artificial (IA) é uma área da ciência da computação que tem revolucionado diversas \
indústrias e aspectos da vida cotidiana. Mas, o que realmente significa "inteligência artificial"? Trata-se de sistemas \
computacionais capazes de realizar tarefas que, anteriormente, só poderiam ser executadas por seres humanos, como \
reconhecimento de fala, tomada de decisão e aprendizado com dados. Impressionante, não é? Esses sistemas utilizam \
algoritmos avançados e grandes volumes de dados para identificar padrões, adaptarem-se a novas situações e fornecerem \
soluções inovadoras.

Um dos maiores avanços recentes em IA é o aprendizado profundo (ou deep learning). Essa técnica permite que máquinas \
realizem tarefas extremamente complexas, como diagnosticar doenças a partir de imagens médicas ou até mesmo compor \
músicas! Curioso como isso funciona? Redes neurais artificiais – inspiradas no funcionamento do cérebro humano – \
processam informações em múltiplas camadas, identificando nuances que seriam impossíveis para métodos tradicionais. \
Como resultado, a IA tem transformado áreas como saúde, finanças e transporte, promovendo eficiência e inovação em \
escala global.

No entanto, a expansão da inteligência artificial também levanta questões importantes. Estamos preparados para lidar \
com os desafios éticos que a IA traz? Por exemplo: como garantir que algoritmos de IA sejam imparciais e inclusivos? \
Além disso, há preocupações sobre o impacto no mercado de trabalho – algumas profissões podem ser substituídas por \
máquinas. Apesar desses desafios, uma coisa é certa: a inteligência artificial já não é mais uma tecnologia do futuro; \
é uma realidade do presente, moldando o mundo ao nosso redor com potencial ilimitado!"""

texto_original = Document(page_content=text)

# Vamos criar agora uma lista de documentos:
docs = [texto_original]

# Criando o splitter usando um modelo 'text-embedding-3-large' da OpenAI
text_splitter = SemanticChunker(OpenAIEmbeddings(model="text-embedding-3-large"))

# Aplicando o split
texts = text_splitter.split_documents(docs)

# Imprimindo o resultado
i = 0
for pedaco in texts:
    print("--" * 30)
    print(f"Chunk: {i}")
    print("--" * 30)
    print(pedaco)
    print("--" * 30)
    i += 1