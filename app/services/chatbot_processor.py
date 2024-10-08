from openai import OpenAI
from app.core.config import settings
from app.core.logging_config import logger


def chatBotStreamingProcessor(message: str,lista_mensagem = []):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    try:
        lista_mensagem.append(
            {"role": "user", "content": message}
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=lista_mensagem
        )
        
        return response.choices[0].message
    except Exception as e:
        logger.error(f"Failed to process document: {str(e)}")
        raise ValueError(f"Failed to process document: {str(e)}")
