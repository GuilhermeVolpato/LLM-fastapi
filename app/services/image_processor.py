import easyocr
from app.core.config import settings
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

def process_image_from_bytes(contents: bytes) -> str:
    try:
        reader = easyocr.Reader(['pt'])
        results = reader.readtext(contents, detail=0, paragraph=True)
        text = " ".join(results)

        llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY, temperature=0.1, model_name="gpt-4-turbo")
        messages = [
            SystemMessage(content="Do que se trata essa foto?"),
            HumanMessage(content=text),
        ]

        response = llm(messages)
        summary = response.content.replace('\n', ' ').strip()
        return summary
    except Exception as e:
        raise ValueError(f"Failed to process image: {str(e)}")
