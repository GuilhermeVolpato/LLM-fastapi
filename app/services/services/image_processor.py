import easyocr
from app.core.config import settings
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.core.logging_config import logger
from openai import OpenAI


# def process_image_from_bytes(contents: bytes) -> str:
#     try:
#         reader = easyocr.Reader(['pt'])
#         results = reader.readtext(contents, detail=0, paragraph=True)
#         text = " ".join(results)

#         llm = ChatOpenAI(openai_api_key=settings.OPENAI_API_KEY,
#                          temperature=0.1, model_name="gpt-4o-mini")
#         messages = [
#             SystemMessage(content="Do que se trata essa foto?"),
#             HumanMessage(content=text),
#         ]
#         response = llm.invoke(messages)
#         summary = response.content.replace('\n', ' ').strip()
#         return summary
#     except Exception as e:
#         logger.error(f"Failed to process image: {str(e)}")
#         raise ValueError(f"Failed to process image: {str(e)}")


def process_image_from_bytes(contents: str, message:str = None) -> str:
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": [
                    {
                        "type": "text",
                        "text": message if message else "O que há nessa imagem?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{contents}"
                        }
                    }
                ]},
            ],
        )

        summary = completion
        print(summary)
        return summary
    except Exception as e:
        logger.error(f"Failed to process image: {str(e)}")
        raise ValueError(f"Failed to process image: {str(e)}")
