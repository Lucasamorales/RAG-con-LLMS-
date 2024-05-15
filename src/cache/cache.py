from langchain_core.caches import BaseCache
from typing import Optional, Sequence, Any


class SimpleCache(BaseCache):
    def __init__(self):
        # Inicializa un diccionario vacío para usar como caché.
        self.cache = {}

    def lookup(self, prompt: str, llm_string: str) -> Optional[Sequence[Any]]:
        # Genera una clave única combinando el prompt y la configuración del modelo (llm_string).
        key = self._generate_key(prompt, llm_string)
        # Retorna el valor guardado en caché para esa clave si existe, de lo contrario retorna None.
        return self.cache.get(key)

    def update(self, prompt: str, llm_string: str, return_val: Sequence[Any]) -> None:
        # Genera una clave única combinando el prompt y la configuración del modelo.
        key = self._generate_key(prompt, llm_string)
        # Guarda el valor de la respuesta en el caché usando la clave generada.
        self.cache[key] = return_val

    def clear(self, **kwargs: Any) -> None:
        # limpia todo el contenido del cache
        self.cache.clear()

    def _generate_key(self, prompt: str, llm_string: str) -> str:
        # Método privado para generar una clave única para el caché basada en el prompt y la configuración del modelo.
        # Esta clave es una combinación del prompt y el llm_string, separados por "::".
        return f"{prompt}::{llm_string}"
