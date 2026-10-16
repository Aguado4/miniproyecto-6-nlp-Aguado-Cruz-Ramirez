# SPEC - Especificación del entregable

> **Estado:** implementado · **Versión:** 1.0 · **Última actualización:** 2026-10-16
>
> Contrato del entregable. Si la implementación se desvía, se actualiza primero este archivo.

---

## 1. Problema

### 1.1 Enunciado

Un **agente de viajes** que no solo busca texto sino que **llama herramientas** expuestas por
servidores **MCP** (*Model Context Protocol*) sobre el corpus turístico de las entregas
anteriores: las reseñas de Rest-Mex y las fichas de destino de Wikipedia del Miniproyecto 5.

> **¿Cuándo conviene una herramienta y cuándo basta con recuperar texto, y sabe el agente
> elegir?**

### 1.2 Por qué esta pregunta

El Miniproyecto 5 montó un RAG sobre este mismo corpus y dejó un límite muy visible: **el RAG
recupera documentos, y hay preguntas que no se responden con documentos**. Si alguien pregunta
«¿cuántas reseñas de 1★ tiene Tulum?» o «¿qué destino tiene la mejor valoración media?», un RAG
trae cinco reseñas y el modelo **estima** la respuesta, que es una forma elegante de inventarla.
Esas preguntas son **agregaciones**, y una agregación se calcula, no se recupera.

Ahí entra MCP. Una herramienta que consulta el `DataFrame` devuelve la cifra **exacta**, y el
agente queda con dos caminos para la misma pregunta. La entrega consiste en construir los dos,
medir cuál acierta en qué, y sobre todo medir **si el agente sabe elegir**, que es el punto donde
los agentes fallan de verdad.

El guía de la Sesión 6 enseña el mecanismo con una calculadora y una API de clima, y lo evalúa
leyendo la traza. Nuestro caso cambia dos cosas: las herramientas operan sobre **nuestros datos**
(así que la respuesta correcta se puede calcular por otro camino y comparar), y la evaluación es
**automática**.

### 1.3 Hipótesis

> **H1 · la agregación necesita herramienta.** En preguntas de conteo, promedio o ranking, el
> agente con herramientas acierta la cifra exacta y el RAG puro de MP5 falla, porque solo ve una
> muestra de cinco documentos. Medible: se compara la respuesta con el valor calculado
> directamente del corpus.
>
> **H2 · el cuello de botella es la elección, no la herramienta.** Las herramientas, una vez
> llamadas, aciertan por construcción. Los errores se concentrarán en que el agente **no llame**
> la herramienta cuando debía, llame la equivocada o invente los argumentos. Medible: tasa de
> selección correcta y de argumentos correctos, leídas de la traza.
>
> **H3 · más herramientas, peor elección.** Al pasar de dos a cuatro herramientas, con descripciones
> que se parecen entre sí, la tasa de selección correcta baja. Es el problema práctico de todo
> sistema con herramientas y la razón por la que las descripciones importan tanto como el código.

### 1.4 Por qué la propuesta es adecuada

1. **Cierra el arco de la serie.** MP1 a MP4 clasificaron la polaridad de este corpus, MP5 lo
   convirtió en fuente de un RAG, y MP6 le añade lo que al RAG le falta: cálculo exacto.
2. **La respuesta correcta es calculable**, así que no hace falta anotación humana ni un LLM de
   juez, con la circularidad que eso trae.
3. **La traza del agente es observable**: `langchain-mcp-adapters` deja ver qué herramienta se
   llamó y con qué argumentos, de modo que H2 y H3 se miden leyendo datos, no impresiones.

## 2. Las herramientas MCP

Cuatro herramientas en dos servidores. El contrato de cada una vive en
[`mcp_servers/README.md`](../mcp_servers/README.md).

| Servidor | Herramienta | Qué hace | Por qué es una herramienta y no RAG |
|---|---|---|---|
| `corpus_mcp_server.py` | `estadisticas_destino` | conteos, media de estrellas y reparto por tipo de un destino | es una agregación: se calcula |
| | `comparar_destinos` | ordena destinos por valoración media, con mínimo de reseñas | es un ranking sobre todo el corpus |
| `busqueda_mcp_server.py` | `buscar_resenas` | búsqueda semántica con filtros de destino, tipo y estrellas | recuperación: aquí sí manda el RAG |
| | `ficha_destino` | devuelve la ficha de Wikipedia de un destino | consulta exacta por clave |

La pareja `estadisticas_destino` / `buscar_resenas` es deliberada: **son la misma pregunta por
dos caminos distintos**, y es donde se ve si el agente entiende la diferencia entre «cuántos» y
«qué dicen».

## 3. Protocolo y métricas

Banco de preguntas propio con la respuesta correcta declarada de forma verificable, siguiendo lo
que funcionó en MP5 (allí fueron metadatos; aquí es la herramienta esperada más el valor exacto).

| Métrica | Qué mide | Hipótesis |
|---|---|---|
| **Exactitud de la cifra** | ¿coincide con el valor calculado del corpus? | H1 |
| **Selección de herramienta** | ¿llamó la que correspondía? | H2 |
| **Argumentos correctos** | ¿pasó bien el destino, el tipo, el rango? | H2 |
| **Llamadas innecesarias** | ¿llamó herramientas que no hacían falta? | H3 |
| **Degradación con 4 herramientas** | las tres anteriores, con 2 y con 4 | H3 |
| **Latencia por llamada** | costo de la ida y vuelta por MCP | contexto |

## 4. Estructura del notebook

Archivo único: `notebooks/miniproyecto6_restmex_mcp.ipynb`

| Sección | Contenido |
|---|---|
| 0 | Portada, problema, resultados principales |
| 1 | Entorno, semilla, Ollama y MCP |
| 2 | El corpus (reutilizado de MP5) y el EDA mínimo que las herramientas necesitan |
| 3 | Qué es MCP y por qué no es «una función más»: servidor, transporte, cliente |
| 4 | Los dos servidores y sus cuatro herramientas, probadas una por una |
| 5 | El banco de preguntas con su respuesta calculada, el calificador y el modelo solo, para ver qué inventa |
| 6 | El agente con herramientas y la lectura de su traza |
| 7 | **Banco de preguntas y evaluación automática** (H1 y H2) |
| 8 | **Dos herramientas frente a cuatro, y cuatro con descripciones de una línea** (H3, D-608) |
| 9 | Comparación con el RAG puro de MP5 en las mismas preguntas |
| 10 | El chatbot en Gradio, con la traza de herramientas visible |
| 11 | Conclusiones y limitaciones |

## 5. Criterios de aceptación

- [x] «Restart & Run All» sin errores, arrancando y apagando los servidores desde el notebook.
- [x] Degrada sin GPU y avisa con claridad si falta Ollama, sin romperse.
- [x] Toda gráfica y tabla con su lectura; conclusiones que responden H1, H2 y H3.
- [x] El chatbot **muestra qué herramienta llamó y con qué argumentos**, no solo la respuesta.
- [x] Celda de Gradio lista para grabar el video.
- [x] Sin `TODO`, `PENDIENTE` ni comentarios de andamiaje.

## 6. Mapa rúbrica → notebook

El detalle de qué hace falta para cada punto está en [`RUBRICA.md`](RUBRICA.md).

| Criterio | Pts | Dónde |
|---|---:|---|
| Notebook completo | 1 | Narrativa por celda, lectura por sección, §11 |
| Reproducibilidad | 2 | Arranque y apagado de servidores, semilla, modelo fijado, corpus en caché |
| ChatBot con herramientas | 2 | §4 a §6, §10 |
| Innovación | 2 | Herramientas sobre datos propios, evaluación automática de la selección (§7), el estudio de 2 contra 4 herramientas (§8), comparación con el RAG de MP5 (§9) |

## 7. Entregable aparte: el video

La consigna exige un **video de máximo 2 minutos** con la celda que levanta Gradio y un par de
interacciones donde se vea que el bot responde **con referencias a lo que usó**. Está en
`results/video/demo_chatbot_mcp.mp4` (D-609). §10 deja la interfaz y un guion de preguntas que muestre una llamada a herramienta
y una respuesta con cita.

## 8. Fuera de alcance

- Entrenar o ajustar modelos: aquí no se entrena nada.
- Herramientas que escriban en sistemas externos; todas son de solo lectura.
- Servidores MCP remotos o de terceros.
