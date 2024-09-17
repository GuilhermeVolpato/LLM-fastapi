from fastapi import FastAPI, File, UploadFile
from typing import List
from pydantic import BaseModel
import fitz  # PyMuPDF para manipulação de documentos PDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.vectorstores.faiss import FAISS
import tiktoken  # Biblioteca para tokenização de texto
from dotenv import load_dotenv
import os
import logging

import time  # Adicionado para testar o tempo de execução

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave da API OpenAI a partir das variáveis de ambiente
openai_api_key = os.getenv("OPENAI_API_KEY")

# Criação da instância FastAPI
app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='servico.log',
    encoding='utf-8',
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

# Modelo de dados para a solicitação de documento (não está sendo usado no código atual)


class DocumentRequest(BaseModel):
    file_path: str

# Função para limpar o texto, removendo espaços extras


def clean_text(text):
    text = " ".join(text.split())  # Remove espaços extras e linhas novas
    return text

# Função para extrair texto das seções do documento PDF


def extract_text_by_sections(pdf_document):
    text_sections = []
    # Itera por cada página do documento PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Carrega a página atual
        blocks = page.get_text("blocks")  # Obtém o texto em blocos
        for block in blocks:
            text = block[4]  # O texto está no índice 4 do bloco
            cleaned_text = clean_text(text)  # Limpa o texto extraído
            # Adiciona o texto limpo à lista
            text_sections.append(cleaned_text)
    return text_sections

# Endpoint para processar o documento PDF


@app.post("/process-document/")
async def process_document(file: UploadFile = File(...)):
    start_time = time.time()
    logging.info("File Name: %s", file.filename)
    try:
        # Abre o documento PDF a partir do arquivo carregado
        pdf_start_time = time.time()

        pdf_document = fitz.open(stream=await file.read())

        pdf_time = time.time() - pdf_start_time
        print(f"Tempo para abrir o PDF: {pdf_time}")
    except Exception as e:
        # Retorna erro se falhar ao ler o PDF
        return {"error": f"Failed to read PDF: {str(e)}"}

    try:
        # Extrai o texto das seções do documento
        extract_start_time = time.time()

        text_sections = extract_text_by_sections(pdf_document)
        # Combina todas as seções de texto em uma única string
        combined_text = " ".join(text_sections)

        extract_time = time.time() - extract_start_time
        print(f"Tempo para extrair o texto: {extract_time}")
    except Exception as e:
        # Retorna erro se falhar ao extrair o texto
        return {"error": f"Failed to extract text: {str(e)}"}

    try:
        # Configura o tokenizador para contar os tokens no texto
        tokenize_start_time = time.time()
        logging.info("Tokenizing text")
        tokenizer = tiktoken.get_encoding("cl100k_base")

        def count_tokens(text: str) -> int:
            # Conta o número de tokens no texto
            return len(tokenizer.encode(text))

        # Configura o splitter de texto para dividir o texto em chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,  # Tamanho do chunk de texto
            chunk_overlap=24,  # Sobreposição entre chunks
            length_function=count_tokens,  # Função para contar tokens
        )

        # Cria documentos divididos a partir do texto combinado
        chunks = text_splitter.create_documents([combined_text])

        tokenize_time = time.time() - tokenize_start_time
        print(f"Tempo para tokenizar o texto: {tokenize_time}")

        # Cria embeddings para os documentos usando OpenAI
        embeddings_start_time = time.time()

        embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key, model="text-embedding-ada-002")
        # Cria um índice FAISS para os documentos, sera usando quando for implementado a busca por similaridade de documentos em nossos banco de dados
        db = FAISS.from_documents(chunks, embeddings)

        embeddings_time = time.time() - embeddings_start_time
        print(f"Tempo para criar embeddings: {embeddings_time}")
        # Configura o modelo de linguagem para gerar o resumo

        summary_start_time = time.time()
        llm = ChatOpenAI(openai_api_key=openai_api_key,
                         temperature=0.1, model_name="gpt-4-turbo",)

        # Combina o conteúdo dos chunks em uma única string
        combined_docs = " ".join([chunk.page_content for chunk in chunks])
        messages = [
            SystemMessage(
                content="Faça um resumo desse documento, logo a baixo do resumo, faça lista de tópicos importantes e no final uma conclusão."),
            HumanMessage(content=combined_docs),
        ]

        # Gera a resposta do modelo de linguagem
        response = llm(messages)
        summary = response.content
        logging.info("Summary: %s", summary)
        # Ajusta a formatação do resumo
        # Substitui quebras de linha por espaços e remove espaços extras
        summary = summary.replace('\n', ' ').strip()
        summary_time = time.time() - summary_start_time
        print(f"Tempo para gerar o resumo: {summary_time}")
        return {"summary": summary}
    except Exception as e:
        # Retorna erro se falhar durante o processamento
        logging.error("Processing error: %s", str(e))
        return {"error": f"Processing error: {str(e)}"}
