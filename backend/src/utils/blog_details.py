import logging

import openai

from src.config import Settings
from src.schemas.blog import BlogPostDetails


logger = logging.getLogger(__name__)

def generate_blog_post_details(transcription: str) -> BlogPostDetails:
    """
    Generate a title, topic, and description for a blog post from the transcription text.
    """
    logger.debug("Configuring OpenAI API key.")
    openai.api_key = Settings().OPENAI_API_KEY

    logger.debug("Generating blog post details from transcription.")
    prompt = f"""
    La siguiente es una transcripción de un video de Instagram:
    "{transcription}"

    A partir de esta transcripción, genera un título para un post en un blog, un tema y una descripción:
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            temperature=0.7,
        )

        output = response['choices'][0]['message']['content'].strip().split("\n")
        logger.debug(f"OpenAI response: {output}")

        title = ""
        topic = ""
        description = ""

        for line in output:
            if line.startswith("Título:"):
                title = line.replace("Título:", "").strip().strip('"')
            elif line.startswith("Tema:"):
                topic = line.replace("Tema:", "").strip()
            elif line.startswith("Descripción:"):
                description = line.replace("Descripción:", "").strip()

        details = BlogPostDetails(
            title=title,
            topic=topic,
            description=description
        )

        return details
    except Exception as e:
        logger.error(f"Error generating blog post details: {e}")
        return None