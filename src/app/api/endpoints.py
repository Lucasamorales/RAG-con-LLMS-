from fastapi import APIRouter, HTTPException
from app.models.request_models import QuestionRequest
from app.core.model import db, model, PROMPT_TEMPLATE
from app.utils.language_detection import detect_language
from langchain_core.prompts import ChatPromptTemplate
from app.cache.cache import SimpleCache

router = APIRouter()
cache = SimpleCache()


@router.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Maneja la solicitud de preguntas del usuario, detecta el idioma, busca el contexto relevante,
    y genera una respuesta utilizando el modelo Cohere.

    Argumentos:
        request (QuestionRequest): La solicitud del usuario que contiene su nombre y la pregunta.

    Retorna:
        dict: Un diccionario con la respuesta generada por el modelo.
    """

    # Detectar el idioma de la pregunta del usuario
    lang_code = detect_language(request.question)

    # Buscar en la base de datos el chunk más relevante
    results = db.similarity_search_with_relevance_scores(request.question, k=1)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron documentos relevantes")

    # Extraer el contexto relevante de los resultados
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    # Verificar si la respuesta está en la cache
    cache_prompt = f"Question: {request.question}\n\ Language:{lang_code}"
    cached_response = cache.lookup(cache_prompt, "ChatCohere")
    if cached_response:
        return {"response": cached_response}

    # Formatear el prompt para el modelo
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=request.question, lang=lang_code)
    print("Prompt enviado al modelo:", prompt)

    # Generar la respuesta del modelo
    response_text = model.invoke(prompt)

    # Almacenar la nueva respuesta en la cache
    cache.update(cache_prompt, "ChatCohere", response_text.content)

    # Devolver la respuesta generada
    return {"response": response_text.content}
