from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from src.cache.cache import SimpleCache
import langid
import os
import uvicorn

app = FastAPI()

# Configuraciond e la API KEY de COHERE
os.environ["COHERE_API_KEY"] = "sfJ8x2tthKmqJManrr3wDCseP5AAqZ8SRykUlens"

# Carga de la base de datos vetorial
CHROMA_PATH = "../Base de datos/chroma"
embedding_function = CohereEmbeddings()
cache = SimpleCache()
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
print(f"Total documentos en la base de datos: {len(db.get()['documents'])}")
# Modelo para generar respuestas:
model = ChatCohere(cache=cache)

# Template de Prompt
PROMPT_TEMPLATE = """
[user_query]
Question: {question}
Language: {lang}

[document_context]
Relevant Information: 
{context}

[response_specifications]
Requirements:
- Respond in the language: {lang}
- Use third person narrative
- Limit the response to one sentence
- Include emojis that summarize the sentiment of the response
- Ensure the response is deterministic and consistent for repeated identical queries
"""


class QuestionRequest(BaseModel):
    user_name: str
    question: str


@app.post("/ask")
def ask_question(request: QuestionRequest):
    def detect_language(text):
        lang, _ = langid.classify(text)
        if lang not in ['es', 'en', 'pt']:
            lang = 'es'  # Asumir español como predeterminado si el idioma detectado no es uno de los permitidos
        return lang

    lang_code = detect_language(request.question)
    # buscar en la base de datos
    results = db.similarity_search_with_relevance_scores(request.question, k=1)
    if not results:
        raise HTTPException(status_code=404, detail="No se encontraron documentos relevantes")

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

    cache_prompt = f"Question: {request.question}\n\ Language:{lang_code}"
    cached_response = cache.lookup(cache_prompt, "ChatCohere")
    if cached_response:
        return{"response": cached_response[0].content}

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=request.question, lang=lang_code)
    print("Prompt enviado al modelo:", prompt)
    # Generar la respuesta del modelo
    response_text = model.invoke(prompt)

    # Almacenar nueva respuesta en cache
    cache.update(cache_prompt, "ChatCohere", response_text.content)

    return {"response": response_text.content}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
