from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_community.vectorstores import Chroma
from app.core.config import CHROMA_PATH
from app.cache.cache import SimpleCache

# Inicialización del embedding function y la base de datos
embedding_function = CohereEmbeddings(model="embed-multilingual-v3.0")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

# Inicialización del modelo
model = ChatCohere(cache=SimpleCache())

# Plantilla de prompt para generar las respuestas del modelo
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
