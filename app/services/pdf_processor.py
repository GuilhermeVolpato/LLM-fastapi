import fitz  # PyMuPDF
from app.core.config import settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.vectorstores.faiss import FAISS
import tiktoken
from app.core.logging_config import logger

def process_pdf(contents: bytes, message: str = None) -> str:
    try:
        pdf_document = fitz.open(stream=contents, filetype="pdf")
        text_sections = extract_text_by_sections(pdf_document)
        combined_text = " ".join(text_sections)

        tokenizer = tiktoken.get_encoding("cl100k_base")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=24,
            length_function=lambda text: len(tokenizer.encode(text)),
        )

        chunks = text_splitter.create_documents([combined_text])
        embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY, model="text-embedding-3-small")
        db = FAISS.from_documents(chunks, embeddings)## caso queira usar o faiss, que serve para consultar banco de dados ou documentos

        llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, temperature=0.1, model_name="gpt-4o-mini",)
        combined_docs = " ".join([chunk.page_content for chunk in chunks])
        messages = [
            SystemMessage(content=message if message else "Me de um resumo de pontos importantes desse pdf"),
            HumanMessage(content=combined_docs),
        ]

        response = llm.invoke(messages)
        summary = response.content.replace('\n', ' ').strip()
        return summary
    except Exception as e:
        logger.error(f"Failed to process PDF: {str(e)}")
        raise ValueError(f"Failed to process PDF: {str(e)}")

def extract_text_by_sections(pdf_document):
    text_sections = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4]
            cleaned_text = " ".join(text.split())
            text_sections.append(cleaned_text)
    return text_sections
