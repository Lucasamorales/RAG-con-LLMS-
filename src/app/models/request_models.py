from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """
    Modelo de datos para las solicitudes de preguntas.

    Atributos:
        user_name (str): Nombre del usuario.
        question (str): Pregunta formulada por el usuario.
    """
    user_name: str
    question: str
