from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langdetect import detect
import os
import uvicorn

app = FastAPI()

# Configuraciond e la API KEY de COHERE
os.environ["COHERE_API_KEY"] = "api key"

# Carga de la base de datos vetorial
CHROMA_PATH = "chroma"
embedding_function = CohereEmbeddings()
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
print(f"Total documentos en la base de datos: {len(db.get()['documents'])}")
# Modelo para generar respuestas:
model = ChatCohere()

# Template de Prompt
PROMPT_TEMPLATE = """
[user_query]
Question: {question} {lang}

[document_context]
Relevant Information: {context} 

[response_specifications]
Answer Requirements: Please respond in {lang}. The response should be  in one sentence, in third person, and include emojis that summarize the sentiment of the response.
"""


class QuestionRequest(BaseModel):
    user_name: str
    question: str


@app.post("/ask")
def ask_question(request: QuestionRequest):
    # identificar enq ue lenguaje esta la pregunta
    query_lang = detect(request.question)
    lang_code = 'en' if query_lang == 'english' else 'es' if query_lang == 'spanish' else 'pt'
    # buscar en la base de datos
    results = db.similarity_search_with_relevance_scores(request.question, k=1)
    if not results:
       raise HTTPException(status_code = 404, detail = "No se encontraron documentos relevantes")

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=request.question, lang=lang_code)
    print("Prompt enviado al modelo:", prompt)
    # Generar la respuesta del modelo
    response_text = model.invoke(prompt)

    return {"response": response_text.content}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
