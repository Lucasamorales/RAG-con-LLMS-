import re


def clean_text(text):
    """
    Limpia el texto eliminando caracteres especiales y convirtiéndolo a minúsculas.

    Argumentos:
        text (str): El texto a limpiar.

    Retorna:
        str: El texto limpio.
    """
    text = text.lower()  # Convertir a minúsculas
    text = re.sub(r"[^a-z0-9áéíóúñ ]", "", text)  # Eliminar caracteres especiales
    return text
