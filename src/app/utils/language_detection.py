import langid


def detect_language(text: str) -> str:
    """
    Detecta el idioma del texto proporcionado.

    Argumentos:
        text (str): El texto cuya lengua será detectada.

    Retorna:
        str: El código del idioma detectado ('es', 'en', 'pt').
    """
    lang, _ = langid.classify(text)
    if lang not in ['es', 'en', 'pt']:
        lang = 'es'  # Asumir español como predeterminado si el idioma detectado no es uno de los permitidos
    return lang
