"""Servidor MCP de recuperación (puerto 9091).

Expone el RAG del Miniproyecto 5 como dos herramientas: búsqueda semántica de reseñas con
filtros de metadatos, y la ficha de Wikipedia de cada destino. Todo lo que devuelve lleva sus
metadatos para que el chatbot pueda citar de dónde sale cada afirmación.
"""

import json
import os

import numpy as np
import pandas as pd
from mcp.server.fastmcp import FastMCP
from sentence_transformers import SentenceTransformer

from comun import DATOS, a_entero, es_vacio, legible, resolver_destino, resolver_tipo

PUERTO = 9091
MODELO_EMBEDDINGS = "intfloat/multilingual-e5-small"
PALABRAS_FICHA = 220  # hay fichas de casi 14.000 palabras: se devuelve solo el inicio

mcp = FastMCP("BusquedaMCP", host="localhost", port=PUERTO)

# Todo se carga una vez al arrancar: el índice, sus vectores, las fichas y el codificador.
INDICE = pd.read_parquet(DATOS / "restmex_indice.parquet")
VECTORES = np.load(DATOS / "vectorstore_e5.npy")
FICHAS = {f["destino"]: f for f in json.loads((DATOS / "fichas_destino.json").read_text("utf-8"))["fichas"]}
DESTINOS = sorted(FICHAS)
CODIFICADOR = SentenceTransformer(MODELO_EMBEDDINGS, device=os.environ.get("MP6_DEVICE", "cpu"))
assert len(INDICE) == len(VECTORES), "El índice y sus vectores no coinciden: recalcula §2."


@mcp.tool()
def buscar_resenas(consulta: str, destino: str | None = None, tipo: str | None = None,
                   estrellas_max: int | None = None, k: int | None = 5) -> str:
    """Busca reseñas REALES de turistas por similitud de significado y devuelve los textos con
    su destino, tipo de lugar y estrellas, para poder citarlos.

    Úsala para preguntas sobre OPINIONES y EXPERIENCIAS: "¿qué dicen de...?", "¿de qué se quejan
    en...?", "¿qué recomiendan comer en...?", "¿cómo es el servicio en...?".
    NO la uses para contar reseñas ni para promedios: solo ve unas pocas reseñas, no todas
    (para cifras: estadisticas_destino o comparar_destinos).

    Args:
        consulta: lo que se busca, en lenguaje natural, por ejemplo "quejas sobre la limpieza".
        destino: filtra por destino, por ejemplo "Tulum"; vacío para buscar en todos.
        tipo: "Hotel", "Restaurant" o "Attractive"; vacío para todos.
        estrellas_max: solo reseñas con como máximo estas estrellas. Usa 2 para buscar quejas.
        k: cuántas reseñas devolver (máximo 10).
    """
    mascara = np.ones(len(INDICE), dtype=bool)
    filtros = []
    if not es_vacio(destino):
        nombre, sugerencias = resolver_destino(destino, DESTINOS)
        if nombre is None:
            pista = f" ¿Quisiste decir: {', '.join(legible(s) for s in sugerencias)}?" if sugerencias else ""
            return f"El destino '{destino}' no está en el corpus.{pista}"
        mascara &= (INDICE["Town"] == nombre).to_numpy()
        filtros.append(f"destino={legible(nombre)}")
    tipo_canonico, valido = resolver_tipo(tipo)
    if not valido:
        return f"Tipo '{tipo}' no reconocido. Usa Hotel, Restaurant o Attractive, o déjalo vacío."
    if tipo_canonico:
        mascara &= (INDICE["Type"] == tipo_canonico).to_numpy()
        filtros.append(f"tipo={tipo_canonico}")
    estrellas_max = a_entero(estrellas_max, None)
    if estrellas_max is not None:
        mascara &= (INDICE["Polarity"] <= estrellas_max).to_numpy()
        filtros.append(f"estrellas<={estrellas_max}")
    k = max(1, min(a_entero(k, 5), 10))

    candidatos = np.flatnonzero(mascara)
    if len(candidatos) == 0:
        return f"No hay reseñas con esos filtros ({', '.join(filtros)})."
    # Prefijo asimétrico de E5: "query: " para la consulta, "passage: " se usó al indexar.
    q = CODIFICADOR.encode(f"query: {consulta}", normalize_embeddings=True)
    similitud = VECTORES[candidatos] @ q
    mejores = candidatos[np.argsort(-similitud)[:k]]

    lineas = [f"{len(mejores)} reseñas más parecidas a '{consulta}'"
              f"{' con filtros ' + ', '.join(filtros) if filtros else ''}:"]
    for i, pos in enumerate(mejores, start=1):
        r = INDICE.iloc[pos]
        texto = " ".join(str(r["Review"]).split())[:350]
        lineas.append(f"[{i}] {legible(r['Town'])} | {r['Type']} | {int(r['Polarity'])} estrellas | "
                      f"\"{r['Title']}\": {texto}")
    return "\n".join(lineas)


@mcp.tool()
def ficha_destino(destino: str) -> str:
    """Devuelve la ficha enciclopédica de Wikipedia de un destino: dónde está, a qué estado
    pertenece, su historia, clima y atractivos, con el título y la URL del artículo para citarlo.

    Úsala para HECHOS sobre el lugar: "¿en qué estado está...?", "¿qué es...?", "¿qué historia
    tiene...?". NO la uses para opiniones de turistas ni para cifras de reseñas.

    Args:
        destino: nombre del destino, por ejemplo "Bacalar" o "Real de Catorce".
    """
    nombre, sugerencias = resolver_destino(destino, DESTINOS)
    if nombre is None:
        pista = f" ¿Quisiste decir: {', '.join(legible(s) for s in sugerencias)}?" if sugerencias else ""
        return f"No hay ficha para '{destino}'.{pista} Fichas disponibles: {', '.join(legible(d) for d in DESTINOS)}."
    ficha = FICHAS[nombre]
    inicio = " ".join(ficha["texto"].split()[:PALABRAS_FICHA])
    return (f"Ficha de {legible(nombre)} | Wikipedia: \"{ficha['titulo_wikipedia']}\" | {ficha['url']}\n"
            f"{inicio}...\n(Licencia CC BY-SA 4.0. Se muestran las primeras {PALABRAS_FICHA} palabras "
            f"de {ficha['palabras']}.)")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
