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

## Estado

**Scaffolding.** Hay diseño, contrato de herramientas y esqueleto de notebook; falta el código de
los servidores y la corrida.

El trabajo está repartido en tres bloques independientes en
[`docs/PLAN.md`](docs/PLAN.md), y lo que tiene que ser verdad para cumplir la rúbrica completa
está en [`docs/RUBRICA.md`](docs/RUBRICA.md).

## Resultados

> Pendiente de la corrida de referencia ([`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md)).

## Cómo ejecutarlo

1. **Ollama** (no es un paquete de Python):
   - Windows y macOS: instalador de <https://ollama.com/download>
   - Linux y Colab: `curl -fsSL https://ollama.com/install.sh | sh`
2. El modelo: `ollama pull llama3.2:3b` (unos 2 GB).
3. Las dependencias: `pip install -r requirements.txt`
4. Abrir `notebooks/miniproyecto6_restmex_mcp.ipynb` y ejecutar de arriba abajo. El notebook
   arranca los servidores MCP y **los apaga al final**; si una ejecución se interrumpe, hay que
   correr la celda de apagado antes de volver a empezar, o el puerto quedará ocupado.

## El video

La consigna exige un video de **máximo 2 minutos** con la celda que levanta Gradio y un par de
interacciones donde el bot responda citando lo que usó. Lo graba el equipo; §10 deja la interfaz y
un guion de preguntas.

> Enlace al video: *pendiente*
