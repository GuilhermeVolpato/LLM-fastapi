from openai import OpenAI
from app.core.config import settings
from app.core.logging_config import logger


def chatBotStreamingProcessor(message: str, lista_mensagem=[], image: str = None, pdf: str = None):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        if image:
            lista_mensagem.append(
                {"role": "user", "content": [
                    {
                        "type": "text",
                        "text": message,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}"
                        }
                    }
                ]}
            )
        elif pdf:
            lista_mensagem.append(
                {"role": "user", "content": [
                    {
                        "type": "text",
                        "text": message,
                    },
                    {
                        "type": "text",
                        "text": pdf
                    }
                ]}
            )
        else:
            lista_mensagem.append(
                {"role": "user", "content": [
                    {
                        "type": "text",
                        "text": message,
                    }
                ]}
            )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=lista_mensagem
        )

        return response.choices[0].message
    except Exception as e:
        logger.error(f"Failed to process document: {str(e)}")
        raise ValueError(f"Failed to process document: {str(e)}")
