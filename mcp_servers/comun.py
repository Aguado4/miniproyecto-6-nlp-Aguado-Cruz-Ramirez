"""Utilidades compartidas por los dos servidores MCP.

El agente escribe los destinos como los diría una persona ("San Cristóbal de las Casas",
"Isla Mujeres", "Todos Santos"), y el corpus los guarda con guiones bajos y sin tildes
("San_Cristobal_de_las_Casas", "TodosSantos"). Este módulo hace el puente entre las dos formas.
"""

import difflib
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "data"

# Sinónimos que el modelo suele usar para los tres tipos de establecimiento del corpus.
TIPOS = {
    "hotel": "Hotel", "hoteles": "Hotel", "hospedaje": "Hotel", "alojamiento": "Hotel",
    "restaurant": "Restaurant", "restaurante": "Restaurant", "restaurantes": "Restaurant",
    "restaurants": "Restaurant", "comida": "Restaurant",
    "attractive": "Attractive", "atraccion": "Attractive", "atracciones": "Attractive",
    "atractivo": "Attractive", "atractivos": "Attractive", "attraction": "Attractive",
    "attractions": "Attractive", "lugar": "Attractive", "lugares": "Attractive",
}

# Valores que un modelo pequeño escribe cuando quiere decir "sin filtro".
VACIOS = {"", "none", "null", "nada", "ninguno", "todos", "todas", "any", "all", "n/a"}


def normalizar(texto: str) -> str:
    """Minúsculas, sin tildes y solo letras y dígitos: 'San Cristóbal' -> 'sancristobal'."""
    sin_tildes = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]", "", sin_tildes.lower())


def es_vacio(valor) -> bool:
    return valor is None or normalizar(valor) in VACIOS


def resolver_destino(nombre: str, destinos: list[str]) -> tuple[str | None, list[str]]:
    """Devuelve (destino del corpus, sugerencias). Si no hay coincidencia exacta, sugiere."""
    clave = normalizar(nombre)
    indice = {normalizar(d): d for d in destinos}
    if clave in indice:
        return indice[clave], []
    # Coincidencia por prefijo: "sancristobal" -> "sancristobaldelascasas".
    por_prefijo = [d for k, d in indice.items() if k.startswith(clave) and len(clave) >= 4]
    if len(por_prefijo) == 1:
        return por_prefijo[0], []
    parecidos = difflib.get_close_matches(clave, list(indice), n=3, cutoff=0.6)
    return None, [indice[p] for p in parecidos]


def resolver_tipo(tipo) -> tuple[str | None, bool]:
    """Devuelve (tipo del corpus o None, es_valido)."""
    if es_vacio(tipo):
        return None, True
    canonico = TIPOS.get(normalizar(tipo))
    return canonico, canonico is not None


def a_entero(valor, por_omision: int | None) -> int | None:
    """El modelo a veces pasa los enteros como texto ("5") o como None en forma de cadena."""
    if es_vacio(valor):
        return por_omision
    try:
        return int(float(valor))
    except (TypeError, ValueError):
        return por_omision


def legible(destino: str) -> str:
    """'Isla_Mujeres' -> 'Isla Mujeres', para que el bot cite nombres legibles."""
    return destino.replace("_", " ")
