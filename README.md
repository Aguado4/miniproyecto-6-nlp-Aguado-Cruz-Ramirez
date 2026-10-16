# Miniproyecto 6 - NLP

**Un agente de viajes con herramientas MCP: cuando recuperar texto no alcanza**

Maestría · Universidad Icesi · Curso de Procesamiento de Lenguaje Natural

Autores: Juan José Aguado · Juan David Cruz · Juan Diego Ramírez

---

## El problema

El [Miniproyecto 5](../miniproyecto%205/) montó un RAG sobre reseñas turísticas y fichas de
Wikipedia, y dejó a la vista un límite: **hay preguntas que no se responden recuperando
documentos**. Si alguien pregunta «¿cuántas reseñas de 1★ tiene Tulum?» o «¿qué destino tiene la
mejor valoración media?», el RAG trae cinco reseñas y el modelo **estima** la respuesta, que es
una forma elegante de inventarla.

Una agregación se calcula, no se recupera. Esta entrega le da al agente herramientas que
calculan, expuestas por **MCP**, y pregunta lo que de verdad importa:

> **¿Cuándo conviene una herramienta y cuándo basta con recuperar texto, y sabe el agente
> elegir?**

- **H1.** En preguntas de agregación, el agente con herramientas acierta la cifra exacta y el RAG
  puro falla.
- **H2.** El cuello de botella no son las herramientas, que aciertan por construcción, sino la
  **elección**: no llamarla, llamar la equivocada o inventar los argumentos.
- **H3.** Al pasar de dos herramientas a cuatro con descripciones parecidas, la elección empeora.

## Por qué este caso

El guía de la sesión enseña MCP con una calculadora y una API de clima, y evalúa el comportamiento
leyendo la traza. Nuestro caso cambia dos cosas, y las dos son deliberadas.

**Las herramientas operan sobre nuestros datos**, así que la respuesta correcta se puede calcular
por un camino independiente (un `groupby` sobre el `DataFrame`) y compararla con lo que dijo el
agente. Con una calculadora no hay nada que medir.

**La evaluación es automática.** El banco de preguntas declara qué herramienta debería llamarse y
con qué argumentos, y se compara con la traza. Eso permite medir la degradación al añadir
herramientas, que es el problema real de todo sistema con *tools* y lo que §8 pone a prueba.

## Las herramientas

| Servidor | Herramienta | Qué hace |
|---|---|---|
| `corpus_mcp_server.py` | `estadisticas_destino` | conteos, media de estrellas y reparto por tipo |
| | `comparar_destinos` | ranking de destinos por valoración media |
| `busqueda_mcp_server.py` | `buscar_resenas` | búsqueda semántica con filtros de metadatos |
| | `ficha_destino` | la ficha de Wikipedia del destino |

Las dos primeras **calculan**; las dos últimas **recuperan**. La pareja
`estadisticas_destino` / `buscar_resenas` es la misma pregunta por dos caminos, y ahí se ve si el
agente entiende la diferencia entre «cuántos» y «qué dicen». Contrato completo en
[`mcp_servers/README.md`](mcp_servers/README.md).

## Resultados

Corrida de referencia del 2026-10-16: 26 preguntas, `llama3.2:3b` en CPU, temperatura 0, 31,8 min
desde cero ([`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md)).

| Camino | Agregación (cifra exacta) | Experiencia (evidencia pertinente) | Hecho (estado correcto) |
|---|---:|---:|---:|
| Modelo solo, sin herramientas | 1 / 12 | sin evidencia | 4 / 6 |
| RAG puro, como en MP5 | 1 / 12 | 0,70 | 6 / 6 |
| **Agente con 4 herramientas MCP** | **11 / 12** | **0,88** | **6 / 6** |

- **H1, confirmada.** Solo el agente da cifras exactas. El modelo solo inventa números «de
  TripAdvisor» y el RAG responde con el número de documentos que recuperó («Bacalar tiene 5
  reseñas»; tiene 10.822).
- **H2, parcial.** La selección fue perfecta (26 de 26). Los errores fueron un argumento inventado,
  una cifra mal leída y un esquema que rechazaba `null` (D-610).
- **H3, refutada tal como se planteó.** Pasar de 2 a 4 herramientas no empeoró la elección (94 % →
  100 %). Lo que la hunde son las **descripciones**: con docstrings de una línea, la selección cae
  al 47 % y la cifra exacta al 0 %.

## El video

**[`results/video/demo_chatbot_mcp.mp4`](results/video/demo_chatbot_mcp.mp4)** (1 min 12 s):
ejecución de la celda que levanta Gradio y dos preguntas. En la primera el bot cita la herramienta
`estadisticas_destino` y las cifras exactas; en la segunda, ocho reseñas con su destino, tipo y
estrellas.

## Cómo ejecutarlo

1. **Ollama** (no es un paquete de Python):
   - Windows y macOS: instalador de <https://ollama.com/download>
   - Linux y Colab: `curl -fsSL https://ollama.com/install.sh | sh`
2. El modelo: `ollama pull llama3.2:3b` (unos 2 GB).
3. Las dependencias, en un entorno nuevo con Python 3.12: `pip install -r requirements.txt`
4. Abrir `notebooks/miniproyecto6_restmex_mcp.ipynb` y ejecutar de arriba abajo. La primera vez
   descarga el corpus y codifica el índice de búsqueda (unos 9 min en CPU); después lo reutiliza.
   El notebook arranca los servidores MCP y **los apaga al final**; si una ejecución se
   interrumpe, la siguiente apaga sola lo que haya quedado vivo antes de arrancar.
5. Opcional: `MP6_SOLO_CPU=1` impide que Ollama use la GPU, como en la corrida de referencia.
