"""Servidor MCP de cálculo sobre el corpus Rest-Mex 2025 (puerto 9090).

Expone dos herramientas que AGREGAN: devuelven cifras exactas calculadas con pandas sobre las
208.051 reseñas, que es justo lo que un RAG no puede dar porque solo ve una muestra.
"""

import pandas as pd
from mcp.server.fastmcp import FastMCP

from comun import DATOS, a_entero, legible, resolver_destino, resolver_tipo

PUERTO = 9090
mcp = FastMCP("CorpusMCP", host="localhost", port=PUERTO)

# El corpus se carga una sola vez al arrancar, no en cada llamada.
CORPUS = pd.read_parquet(DATOS / "restmex.parquet")
DESTINOS = sorted(CORPUS["Town"].unique())
NOMBRE_TIPO = {"Hotel": "hoteles", "Restaurant": "restaurantes", "Attractive": "atracciones"}


def _no_encontrado(destino: str, sugerencias: list[str]) -> str:
    pista = f" ¿Quisiste decir: {', '.join(legible(s) for s in sugerencias)}?" if sugerencias else ""
    return (f"El destino '{destino}' no está en el corpus.{pista} "
            f"Destinos disponibles: {', '.join(legible(d) for d in DESTINOS)}.")


@mcp.tool()
def estadisticas_destino(destino: str) -> str:
    """Calcula cifras EXACTAS de un destino turístico de México a partir de todas sus reseñas:
    número total de reseñas, valoración media (1 a 5 estrellas), cuántas reseñas hay de cada
    número de estrellas y cuántas hay de hoteles, restaurantes y atracciones.

    Úsala para preguntas de CANTIDAD o PROMEDIO sobre UN destino: "¿cuántas reseñas tiene...?",
    "¿qué valoración media tiene...?", "¿cuántas reseñas de 1 estrella...?", "¿cuántos hoteles...?".
    NO la uses para saber qué opinan o qué cuentan los visitantes (para eso: buscar_resenas).

    Args:
        destino: nombre del destino, por ejemplo "Tulum", "Isla Mujeres" o "San Cristóbal de las Casas".
    """
    nombre, sugerencias = resolver_destino(destino, DESTINOS)
    if nombre is None:
        return _no_encontrado(destino, sugerencias)
    sub = CORPUS[CORPUS["Town"] == nombre]
    estrellas = sub["Polarity"].astype(int).value_counts().sort_index()
    lineas = [
        f"Destino: {legible(nombre)} ({legible(sub['Region'].iloc[0])})",
        f"Total de reseñas: {len(sub)}",
        f"Valoración media: {sub['Polarity'].mean():.2f} de 5 estrellas",
        "Reseñas por estrellas: " + " | ".join(
            f"{e} estrella{'s' if e > 1 else ''}: {estrellas.get(e, 0)}" for e in range(1, 6)),
        "Reseñas por tipo: " + " | ".join(
            f"{NOMBRE_TIPO[t]}: {n} (media {sub[sub['Type'] == t]['Polarity'].mean():.2f})"
            for t, n in sub["Type"].value_counts().items()),
        "Fuente: corpus Rest-Mex 2025 completo, cálculo exacto con pandas.",
    ]
    return "\n".join(lineas)


@mcp.tool()
def comparar_destinos(n: int | None = 5, tipo: str | None = None, min_resenas: int | None = 100,
                      peores: bool | None = False) -> str:
    """Ordena TODOS los destinos del corpus por valoración media y devuelve el ranking con la
    media exacta y el número de reseñas de cada uno.

    Úsala para preguntas que COMPARAN destinos: "¿qué destino tiene la mejor valoración?",
    "¿cuáles son los 3 destinos peor valorados?", "¿dónde están los restaurantes mejor valorados?".
    NO la uses para un único destino (para eso: estadisticas_destino).

    Args:
        n: cuántos destinos devolver.
        tipo: "Hotel", "Restaurant" o "Attractive" para comparar solo ese tipo; vacío para todos.
        min_resenas: mínimo de reseñas para entrar al ranking, evita que gane un destino con 3 reseñas.
        peores: True para ordenar de PEOR a mejor valorado ("¿cuál es el peor...?").
    """
    tipo_canonico, valido = resolver_tipo(tipo)
    if not valido:
        return f"Tipo '{tipo}' no reconocido. Usa Hotel, Restaurant o Attractive, o déjalo vacío."
    n = max(1, a_entero(n, 5))
    peores = str(peores).strip().lower() in {"true", "1", "si", "sí", "yes"}
    min_resenas = a_entero(min_resenas, 100)
    sub = CORPUS if tipo_canonico is None else CORPUS[CORPUS["Type"] == tipo_canonico]
    tabla = sub.groupby("Town")["Polarity"].agg(media="mean", resenas="size")
    tabla = tabla[tabla["resenas"] >= min_resenas].sort_values("media", ascending=peores)
    ambito = NOMBRE_TIPO.get(tipo_canonico, "todos los establecimientos")
    orden = "peor" if peores else "mejor"
    lineas = [f"Ranking de destinos {orden} valorados ({ambito}, mínimo {min_resenas} reseñas):"]
    for i, (destino, fila) in enumerate(tabla.head(n).iterrows(), start=1):
        lineas.append(f"{i}. {legible(destino)}: media {fila['media']:.2f} ({int(fila['resenas'])} reseñas)")
    lineas.append(f"Destinos que cumplen el mínimo: {len(tabla)}. Fuente: corpus Rest-Mex 2025, cálculo exacto.")
    return "\n".join(lineas)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
