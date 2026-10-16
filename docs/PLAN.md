# PLAN - Ejecución y reparto del trabajo

> Estado global: **listo para entregar.** Servidores, notebook ejecutado con salidas, métricas,
> figuras y video. Corrida de referencia del 2026-10-16 en `EXPERIMENTS.md`.

Leyenda: `[ ]` pendiente · `[~]` en curso · `[x]` hecho

---

## Fase 0 - Scaffolding (hecho)

- [x] Revisar consigna, rúbrica y los tres notebooks de `icesi-nlp/Sesion6`
- [x] Repositorio y colaboradores
- [x] `SPEC.md` con el caso y las hipótesis, `RUBRICA.md` con el checklist, `DECISIONS.md`
- [x] Contrato de las cuatro herramientas en `mcp_servers/README.md`
- [x] Esqueleto del notebook con las once secciones
- [x] `requirements.txt` y `.gitignore`

## Reparto propuesto

Tres bloques independientes que se pueden trabajar en paralelo sin pisarse, porque tocan
archivos distintos. Lo que los une es el contrato de `mcp_servers/README.md`: si se respeta la
firma de cada herramienta, las tres partes encajan sin negociar nada más.

### Bloque A · Los servidores MCP (`mcp_servers/`)

Quien lo tome escribe Python puro, sin notebook, y puede probarlo con `python
mcp_servers/corpus_mcp_server.py` y un cliente mínimo.

- [x] `corpus_mcp_server.py`: `estadisticas_destino` y `comparar_destinos`
- [x] `busqueda_mcp_server.py`: `buscar_resenas` y `ficha_destino`
- [x] Carga del corpus una sola vez al arrancar el servidor, no por llamada
- [x] Manejo de destino inexistente: mensaje útil, no excepción
- [x] Docstrings cuidados: **son lo que el agente lee para elegir**, así que son parte del
      experimento de H3 y no un adorno

### Bloque B · El notebook, §1 a §6

- [x] §1 entorno: Ollama, MCP, semilla, degradación sin GPU
- [x] §2 corpus y EDA mínimo (se puede copiar de MP5 lo que aplique)
- [x] §3 explicación de MCP: servidor, transporte, cliente, invocación
- [x] §4 arranque y apagado de los servidores, y las cuatro herramientas probadas una por una
- [x] §5 el modelo sin herramientas, para ver qué inventa
- [x] §6 el agente con herramientas y la lectura de la traza

### Bloque C · El notebook, §7 a §11

- [x] §7 banco de preguntas y evaluación automática (H1 y H2)
- [x] §8 dos herramientas frente a cuatro (H3)
- [x] §9 comparación con el RAG de MP5
- [x] §10 chatbot en Gradio con la traza visible, y guion para el video
- [x] §11 conclusiones y limitaciones
- [x] `EXPERIMENTS.md` con los números de la corrida de referencia

### Transversal

- [x] Restart & Run All limpio (lo hace quien cierre)
- [x] **Grabar el video de 2 minutos** (ver `RUBRICA.md` §5)
- [x] Repasar el checklist de `RUBRICA.md` completo antes de entregar

## Riesgos conocidos

Tres cosas que ya nos costaron tiempo en entregas anteriores y que conviene vigilar aquí.

1. **Puertos ocupados.** Si un servidor MCP queda vivo, la siguiente ejecución falla al arrancar
   y eso golpea el criterio de reproducibilidad, que vale 2 puntos. La celda de apagado tiene que
   existir y ser idempotente.
2. **El agente no es determinista por omisión.** Con `temperature` alta elige herramientas
   distintas en cada corrida y los números de §7 no se reproducen. Fijar temperatura baja y
   semilla.
3. **El presupuesto se mide, no se adivina.** En MP4 una corrida «de 20 minutos» resultó ser de
   dos horas. Medir cuánto tarda una pregunta al agente antes de diseñar un banco de 50.

## Presupuesto de tiempo

Medido en la corrida de referencia (CPU, `llama3.2:3b`): una pregunta de agregación cuesta unos
7 s, una de experiencia unos 22 s y una de hechos unos 10 s. El notebook completo, desde cero,
tarda 31,8 min, de los cuales 9 son la codificación del índice de búsqueda.
