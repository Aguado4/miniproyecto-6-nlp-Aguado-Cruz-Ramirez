# CLAUDE.md — Instrucciones de trabajo para este repositorio

Fuente de verdad operativa para cualquier sesión de agente. Léelo completo antes de tocar nada.

---

## 1. Qué es este repositorio

Entregable del **Miniproyecto 6** del curso de NLP (Maestría, Universidad Icesi): **un único
Jupyter Notebook** que construye un **agente de viajes con herramientas MCP** sobre el corpus
turístico de las entregas anteriores, mide si el agente **elige bien la herramienta** y expone el
resultado en una interfaz de Gradio.

Guía: `icesi-nlp/Sesion6/` (`1-herramientas-y-agentes-con-ollama.ipynb`,
`2-mcp-langchain-ollama.ipynb`, `3-chatbot-con-mcp-y-gradio.ipynb` y su carpeta `mcp_servers/`).
**No se usan sus ejemplos**: ni la calculadora ni el clima.

`consigna.txt` y `rubrica.txt` están en la raíz y **no se modifican** (7 puntos, 4 criterios).

### Relación con las entregas anteriores

- Se reutilizan el corpus `vg055/Rest-Mex2025` y las fichas de destino construidas en MP5.
- **No se hereda ningún bloque de celdas** (§D-602), igual que en MP5: aquí no hay clasificación.

## 2. Documentos (leer en este orden)

`docs/SPEC.md` (contrato) · `docs/RUBRICA.md` (**qué tiene que ser verdad para 7,0**) ·
`docs/PLAN.md` (reparto del trabajo) · `docs/DECISIONS.md` (desde D-601) ·
`docs/EXPERIMENTS.md` (solo números ejecutados) · `mcp_servers/README.md` (contrato de las
herramientas).

## 3. Reglas duras

### 3.1 Reproducibilidad — 2 de 7 puntos

- «Restart & Run All» limpio. `SEED = 42` y **temperatura baja en el agente**: con temperatura
  alta elige herramientas distintas en cada corrida y los resultados de §7 no se reproducen.
- **Los servidores MCP se arrancan y se apagan desde el notebook.** La celda de apagado es
  obligatoria y tiene que poder ejecutarse dos veces sin error: un puerto ocupado rompe la
  siguiente ejecución.
- Modelo de Ollama fijado por nombre y etiqueta (`llama3.2:3b`), nunca «el último».
- Sin rutas locales. GPU opcional: en CPU se degrada, nunca falla. Sin Ollama, las secciones de
  agente avisan y se saltan.

### 3.2 Narrativa — 1 punto

Todo en español; markdown antes de cada celda de código explicando el **porqué**; toda gráfica y
tabla con su lectura; **sin guiones largos** en la narrativa. Las lecturas van dentro del markdown
de la sección, no en celdas aparte (lección del MP4). El notebook debe ser **corto**: fue el único
punto de mejora que señaló el profesor en el MP1.

### 3.3 ChatBot con herramientas — 2 puntos

MCP de verdad: servidor, transporte, cliente e invocación visibles. Importar la función
directamente **no es MCP**. El chatbot cita qué herramienta llamó y con qué argumentos.

### 3.4 Innovación — 2 puntos

Herramientas sobre datos propios, evaluación automática de la selección, el estudio de dos
herramientas frente a cuatro, y la comparación con el RAG de MP5 (SPEC §6).

## 4. Convenciones técnicas

- Una herramienta por función, con `@mcp.tool()` y docstring cuidado: **el docstring es lo que el
  agente lee para elegir**, así que es parte del experimento de H3 y no un adorno.
- El corpus se carga una sola vez al arrancar cada servidor, no por llamada.
- `buscar_resenas` reutiliza el codificador de MP5 con sus prefijos asimétricos (`passage: ` y
  `query: `); omitirlos degrada la recuperación de forma silenciosa.
- Toda respuesta que venga de documentos se devuelve con metadatos (destino, tipo, estrellas).

## 5. Qué NO hacer

- No usar la calculadora ni el clima del guía.
- No evaluar «a ojo»: la selección de herramienta se mide leyendo la traza (§D-604).
- No inventar resultados en `EXPERIMENTS.md`.
- No hacer `git push` ni crear releases sin pedirlo al usuario.
- **Sin trailers de IA en los commits** (ni `Co-Authored-By`, ni menciones) en toda la serie.
- No dejar `TODO` ni `PENDIENTE` en el entregable final.
- No ejecutar nada en la GPU sin confirmar: el usuario la usa para otras cosas.

## 6. Pendientes que no dependen del agente

- El **video de 2 minutos** con la demo de Gradio lo graba el equipo. Su ausencia afecta
  considerablemente la calificación (ver `consigna.txt` y `docs/RUBRICA.md` §5).
- El reparto del trabajo entre los tres integrantes está propuesto en `docs/PLAN.md`.
