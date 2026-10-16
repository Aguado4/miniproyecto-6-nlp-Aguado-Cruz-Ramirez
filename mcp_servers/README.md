# Servidores MCP

Contrato de las herramientas. **Este archivo es la interfaz entre los tres bloques de trabajo**
(ver `docs/PLAN.md`): si las firmas se respetan, el notebook y los servidores encajan sin que
haya que ponerse de acuerdo en nada más.

Los servidores siguen la forma del guía (`icesi-nlp/Sesion6/mcp_servers/`): `FastMCP`, una
herramienta por función decorada con `@mcp.tool()`, y transporte `streamable-http` para que
funcione igual en local y en Colab.

```python
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("CorpusMCP", host="localhost", port=9090)

@mcp.tool()
def estadisticas_destino(destino: str) -> str:
    """..."""

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

---

## Puertos

| Servidor | Puerto | Razón |
|---|---:|---|
| `corpus_mcp_server.py` | 9090 | lejos de los 9080 y 9081 del guía, para poder tener los dos |
| `busqueda_mcp_server.py` | 9091 | |

## `corpus_mcp_server.py`

Herramientas de **cálculo** sobre las reseñas. Devuelven cifras exactas, que es justo lo que un
RAG no puede dar.

### `estadisticas_destino(destino: str) -> str`

Conteo de reseñas, media de estrellas, reparto por estrella y por tipo de establecimiento de un
destino.

- `destino`: nombre como aparece en el corpus (`Tulum`, `Isla_Mujeres`, `San_Cristobal_de_las_Casas`).
  **Aceptar también la forma con espacios y sin tildes**, porque es como la escribirá el agente.
- Si el destino no existe, devolver un mensaje con los destinos parecidos, no una excepción.

### `comparar_destinos(n: int = 5, tipo: str | None = None, min_resenas: int = 100, peores: bool = False) -> str`

Ranking de destinos por valoración media.

- `tipo`: `Hotel`, `Restaurant`, `Attractive` o nada para todos.
- `min_resenas`: sin un mínimo, el ranking lo ganan destinos con tres reseñas y el resultado no
  dice nada. El valor por omisión existe por eso.
- `peores`: `True` ordena de peor a mejor valorado (D-606). Un `n` negativo era una convención
  que un modelo de 3B no descubre leyendo el esquema.

## `busqueda_mcp_server.py`

Herramientas de **recuperación**. Son el RAG del Miniproyecto 5 expuesto por MCP.

### `buscar_resenas(consulta: str, destino: str | None = None, tipo: str | None = None, estrellas_max: int | None = None, k: int = 5) -> str`

Búsqueda semántica sobre las reseñas, con filtros de metadatos.

- Reutiliza el codificador de MP5 (`intfloat/multilingual-e5-small`) con sus prefijos
  asimétricos: `passage: ` para los documentos y `query: ` para la consulta. Omitirlos degrada la
  recuperación, y es un error silencioso.
- `estrellas_max` existe por el hallazgo de MP5: los *embeddings* densos recuperan por tema y no
  por polaridad, así que preguntar por quejas devuelve elogios si no se filtra.
- Devolver cada resultado **con sus metadatos** (destino, tipo, estrellas), porque el chatbot
  tiene que poder citarlos y el video tiene que mostrarlo.

### `ficha_destino(destino: str) -> str`

Devuelve la ficha de Wikipedia del destino, leída de `data/fichas_destino.json` (viene del
Miniproyecto 5, con su procedencia y su licencia CC BY-SA).

- Para no desbordar el contexto del modelo, devolver los primeros párrafos y no el artículo
  entero: hay fichas de 13.965 palabras.
- Incluir el título y la URL: es la atribución que la licencia exige y la cita que el bot necesita.

---

## Sobre los docstrings

El agente elige la herramienta leyendo **su nombre y su docstring**. No son documentación para
humanos: son la entrada del clasificador que decide. Dos consecuencias prácticas:

1. Hay que decir explícitamente **cuándo usar la herramienta y cuándo no**. Por ejemplo, en
   `estadisticas_destino` conviene aclarar que sirve para «cuántas» y «qué nota media», no para
   «qué dicen».
2. `estadisticas_destino` y `buscar_resenas` hablan del mismo corpus, así que si sus descripciones
   se parecen demasiado el agente las confundirá. **Esa confusión es justamente lo que mide H3**,
   así que las descripciones no se tocan a mitad del experimento sin anotarlo en
   `docs/DECISIONS.md`.

## Archivos que leen al arrancar

Los genera §2 del notebook y no se versionan: `data/restmex.parquet` (corpus completo),
`data/restmex_indice.parquet` y `data/vectorstore_e5.npy` (índice de búsqueda, D-605). Las fichas
`data/fichas_destino.json` sí se versionan. `comun.py` traduce los nombres que escribe el agente
(«San Cristóbal de las Casas») a los del corpus (`San_Cristobal_de_las_Casas`).

## Cómo probarlos sin el notebook

```bash
# en una terminal, desde mcp_servers/ (después de ejecutar §2 del notebook)
cd mcp_servers && python corpus_mcp_server.py

# en otra, un cliente mínimo
python -c "
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    async with streamable_http_client('http://localhost:9090/mcp') as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            print([t.name for t in (await s.list_tools()).tools])
            print(await s.call_tool('estadisticas_destino', {'destino': 'Tulum'}))

asyncio.run(main())
"
```
