import os
import base64
import io
import re
import fitz
from PIL import Image

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore


from dotenv import load_dotenv
load_dotenv()


class CarregadorDocumento:
    def __init__(self, caminho_documento):
        self.caminho_documento = caminho_documento
        self.text_splitter = RecursiveCharacterTextSplitter(separators = [""], chunk_size=1000, chunk_overlap=200)
        self.embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

    def carregar_texto(self):
        """Lê e carrega o PDF criando os Documents apenas do texto."""
        loader = PyPDFLoader(self.caminho_documento)  # mudar aqui para o caminho do seu computador
        pages_sinc = loader.load()
        return pages_sinc

    def identificar_imagem(self):
        """Identifica a página que tem uma imagem para chamar a função de transcrição depois."""
        paginas_com_imagem = []

        doc_aberto = fitz.open(self.caminho_documento)

        for page_num, page in enumerate(doc_aberto):
            page_text = page.get_text("text")
            # Identifica páginas que contêm figuras baseando-se na presença de legenda: "Figura X - ..."
            if re.search(r'Figura \d+', page_text):
                if page_num not in paginas_com_imagem:
                    paginas_com_imagem.append(page_num)
                    print(f"** Página {page_num+1} contém uma imagem!")

        return paginas_com_imagem

    def gera_transcricao_imagem(self, pagina_com_imagem):
        """ Função que gera a transcrição da imagem usando modelo multimodal e retorna um Document com a descrição
        da imagem."""
        doc_aberto = fitz.open(self.caminho_documento)
        page = doc_aberto.load_page(pagina_com_imagem)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        # Se quiser ver a imagem:
        # img.show()

        # Criar uma instância do modelo Multimodal:
        llm_multimodal = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

        prompt_de_transcricao = """Você é um especialista em criar transcrição fiel da imagem. Comente todos os detalhes. \
Descreva valores e cores quando tiver. Inclua o que a imagem quer apresentar.
Ignore o texto da página, foque na região que contem a imagem. Comentando todos os detalhes como se tivesse explicando \
para uma pessoa cega. Indique também a numeração da imagem que está na legenda."""

        # Cria uma mensagem para ser enviada ao LLM. No caso de imagens é um pouco diferente!
        message = HumanMessage(
            content=[
                {"type": "text", "text": prompt_de_transcricao},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"},
                },
            ],
        )
        response = llm_multimodal.invoke([message])

        return Document(page_content=response.content, metadata={"source":".\DENGUE.pdf", "page":pagina_com_imagem})

    def cria_chunks(self, documentos):
        """Função que cria os chunks"""
        chunks = self.text_splitter.split_documents(documentos)
        return chunks


    def indexar_informacao(self, deseja_indexar_imagem = False):
        """Função cria os embeddings e armazena no banco cloud Qdrant"""
        doc_descr_imagem = []

        # Carrega Imagem se o usuário quiser:
        if deseja_indexar_imagem:
            lista_pg_imagem = self.identificar_imagem()
            for pagina in lista_pg_imagem:
                doc_descr_imagem.append(self.gera_transcricao_imagem(pagina))

        # carrega texto:
        documento_lido = self.carregar_texto()
        chunk_documento_lido = self.cria_chunks(documento_lido)

        todos_documentos = doc_descr_imagem + chunk_documento_lido

        # Indexar no banco vetorial
        QdrantVectorStore.from_documents(
            documents=todos_documentos,
            embedding=self.embedding_model,
            api_key=os.environ.get("QDRANT_API_KEY"),
            url=os.environ.get("QDRANT_URL"),
            prefer_grpc=True,
            collection_name="chatbot_saude"
        )
        print(">> Indexação realizada")


# if __name__=="__main__":
#     i = CarregadorDocumento(r".\DENGUE.pdf")
#     t = i.identificar_imagem()
#     for el in t:
#         t = i.gera_transcricao_imagem(el)
#         print(t)

if __name__=="__main__":
    i = CarregadorDocumento(r".\DENGUE.pdf")
    i.indexar_informacao(True)
