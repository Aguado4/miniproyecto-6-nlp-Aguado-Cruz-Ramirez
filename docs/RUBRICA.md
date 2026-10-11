# RUBRICA - Qué tiene que ser verdad para sacar 7,0 / 7,0

Este documento traduce los cuatro criterios de `rubrica.txt` a cosas **comprobables**. La idea es
que cualquiera del equipo pueda marcar una casilla y que otro pueda verificarla sin discutir.

Incluye lo que aprendimos de la retroalimentación del profesor sobre el Miniproyecto 1
(7,0 / 7,0), cuyo único punto de mejora fue la extensión, y de la experiencia de MP3, MP4 y MP5.

---

## 1. Jupyter Notebook completo · 1 punto

«Celdas de código que implementen el programa solicitado, comentarios detallando el
procedimiento y conclusiones sobre los resultados.»

- [ ] **Markdown antes de cada celda de código** explicando *por qué* se hace, no qué hace.
      El código ya dice qué hace.
- [ ] **Toda tabla y toda gráfica con su lectura debajo**, en prosa, diciendo qué se concluye.
      Una gráfica sin lectura no cuenta.
- [ ] **§11 responde H1, H2 y H3** con un veredicto explícito por hipótesis: confirmada,
      parcial o refutada, con la cifra que lo sostiene.
- [ ] **Limitaciones declaradas**, incluidas las que nos dejan en mal lugar.
- [ ] Cero `TODO`, `PENDIENTE` o comentarios de andamiaje en la versión entregada.
- [ ] Todo en español y **sin guiones largos** en la narrativa (convención de la serie).

**Trampa a evitar, aprendida en MP1:** el profesor señaló que el notebook era *demasiado
extenso*. Secciones que responden a una pregunta cada una, agrupar los estudios comparativos en
una sola sección en lugar de darles una cada uno, y un resumen de resultados en §0 que permita
leer el hallazgo sin recorrer todo.

## 2. Reproducibilidad · 2 puntos

«Todas las celdas ejecutan correctamente y se obtienen los resultados presentados al correr el
notebook desde cero.»

Es el criterio que más puntos da por menos ingenio, así que no se negocia.

- [ ] **Restart & Run All limpio**, verificado de verdad y no de memoria. Dejar constancia de la
      fecha, la máquina y el tiempo total en `EXPERIMENTS.md`.
- [ ] **El notebook se versiona con sus salidas**: quien lo evalúa debe poder leer los resultados
      sin ejecutar nada.
- [ ] **Los servidores MCP se arrancan y se apagan desde el notebook.** Si quedan procesos
      colgados, la segunda ejecución falla por puerto ocupado, y eso es un cero en este criterio.
      Hace falta una celda de apagado y que sea idempotente.
- [ ] **Modelo de Ollama fijado por nombre y etiqueta** (`llama3.2:3b`), nunca «el último».
- [ ] **Semilla fijada** y `temperature` baja en el agente: un agente con temperatura alta elige
      herramientas distintas en cada ejecución y los resultados no se reproducen.
- [ ] **Degradación, no fallo**: sin GPU debe correr más lento pero correr; sin Ollama, las
      secciones de agente deben avisar y saltarse, no reventar.
- [ ] **Sin rutas locales.** Nada de `C:\Users\...`.
- [ ] **Dependencias fijadas** en `requirements.txt`, con las versiones realmente probadas.

**Trampa a evitar, vista en MP5:** una dependencia que falta solo se descubre ejecutando. Probar
en un entorno limpio, no en el que ya tiene todo instalado.

## 3. Implementación del ChatBot · 2 puntos

La rúbrica habla de «modelo de Q&A», que en esta sesión es el **agente con herramientas MCP**.

- [ ] **MCP de verdad, no una función de Python disfrazada.** Tienen que verse las cuatro piezas:
      servidor, transporte, cliente e invocación. Si se importa la función directamente, no es MCP
      y el criterio se cae.
- [ ] **Las cuatro herramientas probadas una por una** antes de entregarlas al agente, con su
      entrada y su salida visibles.
- [ ] **Ejemplos de interacción** que muestren el agente eligiendo herramienta, con la traza.
- [ ] **El chatbot cita lo que usó**: qué herramienta, con qué argumentos y, cuando la respuesta
      viene de documentos, de qué destino y con cuántas estrellas.
- [ ] **Un caso de falla mostrado a propósito**: una pregunta donde el agente elige mal. Mostrar
      el fallo y explicarlo vale más que esconderlo, y la rúbrica premia el manejo de conceptos.
- [ ] **Conceptos usados con precisión**: protocolo, transporte, herramienta, agente, traza.
      Nada de llamar «entrenamiento» a lo que es inferencia.

## 4. Innovación · 2 puntos

«Varias aportaciones valiosas de autoría propia que potencien el trabajo más allá de lo básico.»

El guía hace calculadora y clima, y evalúa leyendo la traza. Nuestras aportaciones:

- [ ] **Herramientas sobre datos propios**, lo que permite calcular la respuesta correcta por
      otro camino y comparar. El guía no puede hacer esto.
- [ ] **Evaluación automática de la selección de herramienta** (§7): tasa de acierto, argumentos
      correctos y llamadas innecesarias, leídas de la traza y no a ojo.
- [ ] **El estudio de 2 frente a 4 herramientas** (§8): cuánto se degrada la elección al añadir
      herramientas parecidas. Es el problema real de los sistemas con herramientas.
- [ ] **Comparación con el RAG de MP5** en las mismas preguntas (§9): cuándo gana la herramienta
      y cuándo la recuperación.
- [ ] **Al menos un hallazgo que contradiga nuestra propia hipótesis**, medido y reportado. En
      MP4 y MP5 fue lo que más valor dio al análisis.

## 5. El video · afecta a toda la nota

- [ ] Máximo **2 minutos**.
- [ ] Se ve **la ejecución de la celda que levanta Gradio**, no solo la interfaz ya abierta.
- [ ] **Un par de interacciones** donde el bot responde **con referencias** a lo que usó.
- [ ] Enlace en el README y en la entrega de Intu.

**Esto no lo puede hacer el agente: lo graba el equipo.** La consigna dice que su ausencia
«afecta negativa y considerablemente» la calificación.

## 6. Antes de entregar

- [ ] Restart & Run All desde cero, en una máquina donde no quede nada corriendo.
- [ ] `EXPERIMENTS.md` con los números de esa corrida y de ninguna otra.
- [ ] `PLAN.md` sin tareas abiertas que importen.
- [ ] Ningún proceso de servidor MCP vivo al terminar.
- [ ] Enlace del video puesto.
- [ ] Commits sin trailers de IA, como en toda la serie.
