from langchain_core.caches import BaseCache
from typing import Optional, Sequence, Any


class SimpleCache(BaseCache):
    def __init__(self):
        """
        Inicializa una instancia de SimpleCache con un diccionario vacío para usar como caché.
        """
        self.cache = {}

    def lookup(self, prompt: str, llm_string: str) -> Optional[Sequence[Any]]:
        """
        Busca en el caché una respuesta almacenada previamente para un prompt y configuración de modelo dados.

        Argumentos:
            prompt (str): El prompt usado para generar la respuesta.
            llm_string (str): La configuración del modelo de lenguaje.

        Retorna:
            Optional[Sequence[Any]]: La respuesta almacenada en caché si existe, de lo contrario None.
        """
        # Genera una clave única combinando el prompt y la configuración del modelo (llm_string).
        key = self._generate_key(prompt, llm_string)
        # Retorna el valor guardado en caché para esa clave si existe, de lo contrario retorna None.
        return self.cache.get(key)

    def update(self, prompt: str, llm_string: str, return_val: Sequence[Any]) -> None:
        """
        Actualiza el caché con una nueva respuesta para un prompt y configuración de modelo dados.

        Argumentos:
            prompt (str): El prompt usado para generar la respuesta.
            llm_string (str): La configuración del modelo de lenguaje.
            return_val (Sequence[Any]): La respuesta generada que se guardará en el caché.

        Retorna:
            None
        """
        # Genera una clave única combinando el prompt y la configuración del modelo.
        key = self._generate_key(prompt, llm_string)
        # Guarda el valor de la respuesta en el caché usando la clave generada.
        self.cache[key] = return_val

    def clear(self, **kwargs: Any) -> None:
        """
        Limpia todo el contenido del caché.

        Argumentos:
            kwargs (Any): Argumentos adicionales opcionales.

        Retorna:
            None
        """
        # Limpia todo el contenido del caché.
        self.cache.clear()

    def _generate_key(self, prompt: str, llm_string: str) -> str:
        """
        Genera una clave única para el caché basada en el prompt y la configuración del modelo.

        Argumentos:
            prompt (str): El prompt usado para generar la respuesta.
            llm_string (str): La configuración del modelo de lenguaje.

        Retorna:
            str: La clave generada para el caché.
        """
        # Esta clave es una combinación del prompt y el llm_string, separados por "::".
        return f"{prompt}::{llm_string}"
