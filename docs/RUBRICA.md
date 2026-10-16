# RUBRICA - Qué tiene que ser verdad para sacar 7,0 / 7,0

Este documento traduce los cuatro criterios de `rubrica.txt` a cosas **comprobables**. La idea es
que cualquiera del equipo pueda marcar una casilla y que otro pueda verificarla sin discutir.

Incluye lo que aprendimos de la retroalimentación del profesor sobre el Miniproyecto 1
(7,0 / 7,0), cuyo único punto de mejora fue la extensión, y de la experiencia de MP3, MP4 y MP5.

---

## 1. Jupyter Notebook completo · 1 punto

«Celdas de código que implementen el programa solicitado, comentarios detallando el
procedimiento y conclusiones sobre los resultados.»

- [x] **Markdown antes de cada celda de código** explicando *por qué* se hace, no qué hace.
      El código ya dice qué hace.
- [x] **Toda tabla y toda gráfica con su lectura debajo**, en prosa, diciendo qué se concluye.
      Una gráfica sin lectura no cuenta.
- [x] **§11 responde H1, H2 y H3** con un veredicto explícito por hipótesis: confirmada,
      parcial o refutada, con la cifra que lo sostiene.
- [x] **Limitaciones declaradas**, incluidas las que nos dejan en mal lugar.
- [x] Cero `TODO`, `PENDIENTE` o comentarios de andamiaje en la versión entregada.
- [x] Todo en español y **sin guiones largos** en la narrativa (convención de la serie).

**Trampa a evitar, aprendida en MP1:** el profesor señaló que el notebook era *demasiado
extenso*. Secciones que responden a una pregunta cada una, agrupar los estudios comparativos en
una sola sección en lugar de darles una cada uno, y un resumen de resultados en §0 que permita
leer el hallazgo sin recorrer todo.

## 2. Reproducibilidad · 2 puntos

«Todas las celdas ejecutan correctamente y se obtienen los resultados presentados al correr el
notebook desde cero.»

Es el criterio que más puntos da por menos ingenio, así que no se negocia.

- [x] **Restart & Run All limpio**, verificado de verdad y no de memoria. Dejar constancia de la
      fecha, la máquina y el tiempo total en `EXPERIMENTS.md`.
- [x] **El notebook se versiona con sus salidas**: quien lo evalúa debe poder leer los resultados
      sin ejecutar nada.
- [x] **Los servidores MCP se arrancan y se apagan desde el notebook.** Si quedan procesos
      colgados, la segunda ejecución falla por puerto ocupado, y eso es un cero en este criterio.
      Hace falta una celda de apagado y que sea idempotente.
- [x] **Modelo de Ollama fijado por nombre y etiqueta** (`llama3.2:3b`), nunca «el último».
- [x] **Semilla fijada** y `temperature` baja en el agente: un agente con temperatura alta elige
      herramientas distintas en cada ejecución y los resultados no se reproducen.
- [x] **Degradación, no fallo**: sin GPU debe correr más lento pero correr; sin Ollama, las
      secciones de agente deben avisar y saltarse, no reventar.
- [x] **Sin rutas locales.** Nada de `C:\Users\...`.
- [x] **Dependencias fijadas** en `requirements.txt`, con las versiones realmente probadas.

**Trampa a evitar, vista en MP5:** una dependencia que falta solo se descubre ejecutando. Probar
en un entorno limpio, no en el que ya tiene todo instalado.

## 3. Implementación del ChatBot · 2 puntos

La rúbrica habla de «modelo de Q&A», que en esta sesión es el **agente con herramientas MCP**.

- [x] **MCP de verdad, no una función de Python disfrazada.** Tienen que verse las cuatro piezas:
      servidor, transporte, cliente e invocación. Si se importa la función directamente, no es MCP
      y el criterio se cae.
- [x] **Las cuatro herramientas probadas una por una** antes de entregarlas al agente, con su
      entrada y su salida visibles.
- [x] **Ejemplos de interacción** que muestren el agente eligiendo herramienta, con la traza.
- [x] **El chatbot cita lo que usó**: qué herramienta, con qué argumentos y, cuando la respuesta
      viene de documentos, de qué destino y con cuántas estrellas.
- [x] **Un caso de falla mostrado a propósito**: una pregunta donde el agente elige mal. Mostrar
      el fallo y explicarlo vale más que esconderlo, y la rúbrica premia el manejo de conceptos.
- [x] **Conceptos usados con precisión**: protocolo, transporte, herramienta, agente, traza.
      Nada de llamar «entrenamiento» a lo que es inferencia.

## 4. Innovación · 2 puntos

«Varias aportaciones valiosas de autoría propia que potencien el trabajo más allá de lo básico.»

El guía hace calculadora y clima, y evalúa leyendo la traza. Nuestras aportaciones:

- [x] **Herramientas sobre datos propios**, lo que permite calcular la respuesta correcta por
      otro camino y comparar. El guía no puede hacer esto.
- [x] **Evaluación automática de la selección de herramienta** (§7): tasa de acierto, argumentos
      correctos y llamadas innecesarias, leídas de la traza y no a ojo.
- [x] **El estudio de 2 frente a 4 herramientas** (§8): cuánto se degrada la elección al añadir
      herramientas parecidas. Es el problema real de los sistemas con herramientas.
- [x] **Comparación con el RAG de MP5** en las mismas preguntas (§9): cuándo gana la herramienta
      y cuándo la recuperación.
- [x] **Al menos un hallazgo que contradiga nuestra propia hipótesis**, medido y reportado. En
      MP4 y MP5 fue lo que más valor dio al análisis.

## 5. El video · afecta a toda la nota

- [x] Máximo **2 minutos**.
- [x] Se ve **la ejecución de la celda que levanta Gradio**, no solo la interfaz ya abierta.
- [x] **Un par de interacciones** donde el bot responde **con referencias** a lo que usó.
- [x] Enlace en el README.
- [ ] Adjunto o enlace en la entrega de Intu (lo hace el equipo al entregar).

Grabado y versionado en `results/video/demo_chatbot_mcp.mp4` (1 min 12 s, D-609). Falta solo
adjuntarlo en Intu o subirlo a una plataforma y pegar el enlace en la entrega.

## 6. Antes de entregar

- [x] Restart & Run All desde cero, en una máquina donde no quede nada corriendo.
- [x] `EXPERIMENTS.md` con los números de esa corrida y de ninguna otra.
- [x] `PLAN.md` sin tareas abiertas que importen.
- [x] Ningún proceso de servidor MCP vivo al terminar.
- [x] Enlace del video puesto en el README; falta en Intu.
- [x] Commits sin trailers de IA, como en toda la serie.
