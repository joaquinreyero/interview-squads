from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import requests
from langchain import OpenAI
from langchain.prompts import PromptTemplate

router = APIRouter()

class ReelLink(BaseModel):
    link: str

class BlogPost(BaseModel):
    content: str
    title: str
    excerpt: str
    slug: str

@router.post("/generate_blog_post")
async def generate_blog_post(reel_link: ReelLink):
    # Verificar que el link sea válido
    if "instagram.com/reel/" not in reel_link.link:
        raise HTTPException(status_code=400, detail="Invalid Instagram reel link")

    # Mockear el contenido del reel en lugar de usar Selenium
    reel_content = (
        "Hoy compartimos los 5 mejores consejos para lanzar tu startup con éxito. "
        "Primero, asegúrate de validar tu idea con tu público objetivo. "
        "Segundo, construye un equipo sólido con habilidades complementarias. "
        "Tercero, crea un plan de negocio detallado y realista. "
        "Cuarto, busca financiación adecuada y establece relaciones con inversores. "
        "Quinto, no tengas miedo de pivotar y adaptarte a los cambios del mercado. "
        "Estos consejos son esenciales para cualquier emprendedor que quiera tener éxito en el competitivo mundo de las startups. "
        "¡No te olvides de seguirnos para más consejos y contenido inspirador!"
    )

    # Configurar la API de LangChain con OpenAI
    openai_api_key = "sk-proj-gg2QQVv3Gzq7Mop9VlwyT3BlbkFJQhBJWZzH02qx7ml0kB3n"
    if not openai_api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not found")

    openai = OpenAI(api_key=openai_api_key)
    prompt_template = PromptTemplate(
        input_variables=["reel_content"],
        template="Genera un post de blog basado en el siguiente contenido del reel de Instagram: {reel_content}"
    )
    prompt = prompt_template.format(reel_content=reel_content)

    try:
        response = openai(prompt, max_tokens=500)
        generated_text = response['choices'][0]['text'].strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating blog post: {e}")

    # Parsear la respuesta de GPT-4
    blog_post = BlogPost(
        content=generated_text,
        title="Título generado automáticamente",  # Puedes usar lógica adicional para generar un título
        excerpt=generated_text[:100],  # Extracto del contenido, los primeros 100 caracteres
        slug="slug-generado-automaticamente"  # Puedes generar un slug basado en el título o contenido
    )

    # Enviar la solicitud POST a jsonplaceholder.typicode.com/posts
    try:
        response = requests.post(
            "https://jsonplaceholder.typicode.com/posts",
            json=blog_post.dict()
        )
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating blog post: {e}")

    return blog_post.dict()
